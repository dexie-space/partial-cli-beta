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
    PartialInfo,
    get_launcher_or_partial_cs,
    get_partial_info,
    get_puzzle,
    process_taker_offer,
)


# take
@click.command("take", help="take the dexie partial offer.")
@click.option(
    "-f",
    "--fingerprint",
    required=True,
    help="Set the fingerprint to specify which wallet to use",
    type=int,
)
@click.option(
    "-a",
    "--taken_mojos",
    required=True,
    default=None,
    help="Taken amount in mojos",
    type=uint64,
)
@click.argument("offer_file", type=click.File("r"), required=True)
@click.pass_context
def take_cmd(ctx, fingerprint, taken_mojos, offer_file):

    offer_bech32 = offer_file.read()
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

    if partial_info.offer_mojos < taken_mojos:
        print(
            f"Requested amount, {taken_mojos} mojos is greater than the offer amount, {partial_info.offer_mojos} mojos."
        )
        return

    offer_cat_mojos = uint64(taken_mojos * partial_info.rate * 1e-12)
    total_request_cat_mojos = partial_info.offer_mojos * partial_info.rate * 1e-12
    print("Dexie Partial Offer Summary:")
    print("============================")
    print(f"Total Offer Amount: {partial_info.offer_mojos/1e12} XCH")
    print(f"Total Request Amount: {total_request_cat_mojos/1e3} CATs")
    print(f"Rate: {partial_info.rate/1e3} CATs -> 1 XCH")
    print(f"Sending {offer_cat_mojos/1e3} CATs")
    print(f"Receiving {taken_mojos/1e12} XCH")

    is_confirmed = Confirm.ask("Would you like to take this offer?")

    if not is_confirmed:
        return
    else:
        asyncio.run(
            take_partial_offer(
                sb if launcher_coin is not None else None,
                partial_coin,
                partial_info,
                fingerprint,
                taken_mojos,
            )
        )


async def create_taker_offer(
    partial_info: PartialInfo,
    fingerprint: int,
    taken_mojos: uint64,
):
    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):

        tail_hash = partial_info.tail_hash.hex()
        request_cat_mojos = uint64(taken_mojos * partial_info.rate * 1e-12)
        offer_dict = {
            "1": taken_mojos,
            tail_hash: -1 * request_cat_mojos,
        }

        offer, tx_record = await wallet_rpc_client.create_offer_for_ids(
            offer_dict=offer_dict, tx_config=DEFAULT_TX_CONFIG, validate_only=False
        )
        if offer is None:
            raise Exception("Failed to create offer")

        return offer, request_cat_mojos


async def take_partial_offer(
    create_offer_coin_sb: Optional[SpendBundle],
    partial_coin: Coin,
    partial_info: PartialInfo,
    fingerprint: int,
    taken_mojos: uint64,
):
    partial_coin_id = partial_coin.name()
    taker_offer, request_cat_mojos = await create_taker_offer(
        partial_info, fingerprint, taken_mojos
    )

    # create spend bundle
    p = get_puzzle(
        partial_info.maker_puzzle_hash,
        partial_info.public_key,
        partial_info.tail_hash,
        partial_info.rate,
        partial_info.offer_mojos,
    )
    s = Program.to([partial_coin_id, taken_mojos])

    eph_partial_cs: CoinSpend = make_spend(partial_coin, puzzle_reveal=p, solution=s)

    maker_request_payments = Program.to(
        [
            partial_coin_id,
            [
                partial_info.maker_puzzle_hash,
                request_cat_mojos,
                [partial_info.maker_puzzle_hash],
            ],
        ]
    )
    (
        taker_coin_spends,
        taker_request_payments,
        taker_offer_sig,
    ) = process_taker_offer(taker_offer, maker_request_payments)

    paritial_offer_sb = SpendBundle(
        [
            eph_partial_cs,
            make_spend(
                Coin(
                    parent_coin_info=eph_partial_cs.coin.name(),
                    puzzle_hash=OFFER_MOD_HASH,
                    amount=taken_mojos,
                ),
                OFFER_MOD,
                taker_request_payments,
            ),
        ]
        + taker_coin_spends,
        taker_offer_sig,
    )

    sb = (
        SpendBundle.aggregate([create_offer_coin_sb, paritial_offer_sb])
        if create_offer_coin_sb
        else paritial_offer_sb
    )

    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):
        await wallet_rpc_client.push_tx(sb)

    ret = {
        "spend_bundle": sb.to_json_dict(),
    }
    new_offer_mojos = partial_info.offer_mojos - taken_mojos
    if new_offer_mojos > 0:
        # create next offer file if needed
        next_puzzle = get_puzzle(
            partial_info.maker_puzzle_hash,
            partial_info.public_key,
            partial_info.tail_hash,
            partial_info.rate,
            partial_info.offer_mojos - taken_mojos,
        )
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
        ret["next_offer"] = next_offer.to_bech32()

    print(json.dumps(ret, indent=2))
