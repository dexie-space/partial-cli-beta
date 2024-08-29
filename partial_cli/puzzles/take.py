import asyncio
import json
from rich.prompt import Confirm
import rich_click as click
from typing import Optional

from chia.cmds.cmds_util import get_wallet_client
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.coin_spend import CoinSpend, make_spend
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint64
from chia.wallet.trading.offer import OFFER_MOD, OFFER_MOD_HASH, Offer
from chia.wallet.util.tx_config import DEFAULT_COIN_SELECTION_CONFIG, DEFAULT_TX_CONFIG

from chia_rs import G2Element

from partial_cli.config import wallet_rpc_port
from partial_cli.puzzles.partial import (
    FEE_MOD,
    PartialInfo,
    display_partial_info,
    get_launcher_or_partial_cs,
    get_partial_info,
    process_taker_offer,
)


async def create_taker_offer(
    partial_info: PartialInfo,
    fingerprint: int,
    request_mojos_minus_fees: uint64,
    offer_cat_mojos: uint64,
    blockchain_fee_mojos: uint64,
):
    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):

        tail_hash = partial_info.tail_hash.hex()
        offer_dict = {
            "1": request_mojos_minus_fees,
            tail_hash: -1 * offer_cat_mojos,
        }

        offer, tx_record = await wallet_rpc_client.create_offer_for_ids(
            offer_dict=offer_dict,
            tx_config=DEFAULT_TX_CONFIG,
            validate_only=False,
            fee=blockchain_fee_mojos,
        )
        if offer is None:
            raise Exception("Failed to create offer")

        return offer


async def take_partial_offer(
    taker_offer: Offer,
    create_offer_coin_sb: Optional[SpendBundle],
    partial_coin: Coin,
    partial_info: PartialInfo,
    request_mojos: uint64,
    fee_mojos: uint64,
    offer_cat_mojos: uint64,
    blockchain_fee_mojos: uint64,
):
    partial_coin_id = partial_coin.name()
    # only request the amount minus fees
    request_mojos_minus_fees = request_mojos - fee_mojos

    # create spend bundle
    p = partial_info.to_partial_puzzle()
    s = Program.to([partial_coin_id, request_mojos])

    eph_partial_cs: CoinSpend = make_spend(partial_coin, puzzle_reveal=p, solution=s)

    maker_request_payments = Program.to(
        [
            partial_coin_id,
            [
                partial_info.maker_puzzle_hash,
                offer_cat_mojos,
                [partial_info.maker_puzzle_hash],
            ],
        ]
    )
    (
        taker_coin_spends,
        taker_request_payments,
        taker_offer_sig,
    ) = process_taker_offer(taker_offer, maker_request_payments)

    partial_offer_sb = SpendBundle(
        [
            eph_partial_cs,
            make_spend(
                Coin(
                    parent_coin_info=eph_partial_cs.coin.name(),
                    puzzle_hash=OFFER_MOD_HASH,
                    amount=request_mojos_minus_fees,
                ),
                OFFER_MOD,
                taker_request_payments,
            ),
        ]
        + taker_coin_spends,
        taker_offer_sig,
    )

    sb = (
        SpendBundle.aggregate([create_offer_coin_sb, partial_offer_sb])
        if create_offer_coin_sb
        else partial_offer_sb
    )

    new_offer_mojos = partial_info.offer_mojos - request_mojos
    if new_offer_mojos > 0:
        # create next offer file if needed
        next_partial_info = PartialInfo(
            partial_info.fee_puzzle_hash,
            partial_info.fee_rate,
            partial_info.maker_puzzle_hash,
            partial_info.public_key,
            partial_info.tail_hash,
            partial_info.rate,
            new_offer_mojos,
        )

        next_puzzle = next_partial_info.to_partial_puzzle()
        next_offer_cs = make_spend(
            coin=Coin(
                parent_coin_info=partial_coin.name(),
                puzzle_hash=next_puzzle.get_tree_hash(),
                amount=new_offer_mojos,
            ),
            puzzle_reveal=next_puzzle,
            solution=Program.to([]),
        )

        next_offer_sb = SpendBundle([next_offer_cs], G2Element())
        next_offer = Offer.from_spend_bundle(next_offer_sb)
        return sb, next_offer
    else:
        return sb, None


def get_offer_values(partial_info: PartialInfo, request_mojos: uint64):
    fee_mojos = FEE_MOD.run(Program.to([partial_info.fee_rate, request_mojos])).as_int()
    offer_cat_mojos = uint64(request_mojos * partial_info.rate * 1e-12)
    return fee_mojos, offer_cat_mojos


async def take_cmd_async(
    create_offer_coin_sb: Optional[SpendBundle],
    partial_coin: Coin,
    partial_info: PartialInfo,
    fingerprint: int,
    request_mojos: uint64,
    fee_mojos: uint64,
    offer_cat_mojos: uint64,
    blockchain_fee_mojos: uint64,
    taker_offer: Optional[Offer] = None,
):
    if taker_offer is None:
        taker_offer = await create_taker_offer(
            partial_info,
            fingerprint,
            request_mojos - fee_mojos,
            offer_cat_mojos,
            blockchain_fee_mojos,
        )

    sb, next_offer = await take_partial_offer(
        taker_offer=taker_offer,
        create_offer_coin_sb=create_offer_coin_sb,
        partial_coin=partial_coin,
        partial_info=partial_info,
        request_mojos=request_mojos,
        fee_mojos=fee_mojos,
        offer_cat_mojos=offer_cat_mojos,
        blockchain_fee_mojos=blockchain_fee_mojos,
    )

    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):
        await wallet_rpc_client.push_tx(sb)

    ret = {"spend_bundle": sb.to_json_dict()}
    if next_offer is not None:
        ret["next_offer"] = next_offer.to_bech32()
    print(json.dumps(ret, indent=2))


# take
@click.command(
    "take",
    help="Take the dexie partial offer by providing the taker offer file or request information.",
)
@click.option(
    "-f",
    "--fingerprint",
    required=True,
    help="Set the fingerprint to specify which wallet to use",
    type=int,
)
@click.option(
    "-o",
    "--offer-file",
    "taker_offer_file",
    help="Taker offer file",
    required=False,
    type=click.File("r"),
)
@click.option(
    "-r",
    "--request-information",
    required=False,
    nargs=2,
    help="Request XCH amount and blockchain fee in mojos (e.g., -r 100000000000 1000)",
    type=click.Tuple([uint64, uint64]),
)
@click.argument("partial_offer_file", type=click.File("r"), required=True)
@click.pass_context
def take_cmd(
    ctx,
    fingerprint,
    taker_offer_file,
    request_information,
    partial_offer_file,
):
    if taker_offer_file is None and request_information is None:
        print("Either offer file or request information is required.")
        return

    offer_bech32 = partial_offer_file.read()
    offer: Offer = Offer.from_bech32(offer_bech32)
    sb: SpendBundle = offer.to_spend_bundle()

    cs, is_spent = asyncio.run(get_launcher_or_partial_cs(sb.coin_spends))
    if is_spent:
        print("Partial offer is not valid")
        return

    partial_coin, partial_info, launcher_coin = get_partial_info(cs)

    if partial_info is None:
        print("Partial offer is not valid")
        return

    # calculate request amounts and fees
    if taker_offer_file is not None:
        taker_offer_bech32 = taker_offer_file.read()
        taker_offer: Offer = Offer.from_bech32(taker_offer_bech32)
        request_amounts = taker_offer.get_requested_amounts()
        assert len(request_amounts) == 1
        assert None in request_amounts
        request_mojos_minus_fees = taker_offer.get_requested_amounts()[None]
        blockchain_fee_mojos = taker_offer.fees()
        request_mojos = uint64(
            request_mojos_minus_fees / (1 - (partial_info.fee_rate / 1e4))
        )
        fee_mojos = int(request_mojos - request_mojos_minus_fees)
        offer_cat_mojos = uint64(request_mojos * partial_info.rate * 1e-12)
    else:
        request_mojos, blockchain_fee_mojos = request_information
        if partial_info.offer_mojos < request_mojos:
            print(
                f"Requested amount, {request_mojos} mojos is greater than the offer amount, {partial_info.offer_mojos} mojos."
            )
            return

        fee_mojos, offer_cat_mojos = get_offer_values(partial_info, request_mojos)
        request_mojos_minus_fees = request_mojos - fee_mojos

    display_partial_info(partial_info, partial_coin.name(), is_valid=not is_spent)
    print("")
    print(f" {offer_cat_mojos/1e3} CATs -> {request_mojos/1e12} XCH")
    print(f" Sending {offer_cat_mojos/1e3} CATs")
    print(f" Paying {fee_mojos/1e12} XCH in fees")
    print(f" Receiving {request_mojos_minus_fees/1e12} XCH")

    is_confirmed = Confirm.ask("\n Would you like to take this offer?")

    if not is_confirmed:
        return
    else:
        asyncio.run(
            take_cmd_async(
                create_offer_coin_sb=sb if launcher_coin is not None else None,
                partial_coin=partial_coin,
                partial_info=partial_info,
                fingerprint=fingerprint,
                request_mojos=request_mojos,
                fee_mojos=fee_mojos,
                offer_cat_mojos=offer_cat_mojos,
                blockchain_fee_mojos=blockchain_fee_mojos,
                taker_offer=taker_offer if taker_offer_file is not None else None,
            )
        )
