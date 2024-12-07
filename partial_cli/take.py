import asyncio
import json
from rich.prompt import Confirm
import rich_click as click
from typing import Any, Dict, List, Optional

from chia.cmds.cmds_util import get_wallet_client
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend, make_spend
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint64
from chia.wallet.cat_wallet.cat_utils import (
    CAT_MOD,
    SpendableCAT,
    match_cat_puzzle,
    unsigned_spend_bundle_for_spendable_cats,
)
from chia.wallet.lineage_proof import LineageProof
from chia.wallet.trading.offer import OFFER_MOD, OFFER_MOD_HASH, ZERO_32, Offer
from chia.wallet.uncurried_puzzle import uncurry_puzzle
from chia.wallet.util.tx_config import DEFAULT_TX_CONFIG

from partial_cli.config import wallet_rpc_port
from partial_cli.puzzles import (
    FEE_MOD,
    get_create_offer_coin_sb,
    get_partial_coin_parent_coin_spend,
    get_partial_coin_spend,
    get_partial_spendable_cat,
)
from partial_cli.types.partial_info import PartialInfo
from partial_cli.utils.partial import display_partial_info, get_amount_str
from partial_cli.utils.rpc import is_coin_spent
from partial_cli.utils.shared import get_wallet


# taking CAT offer
# taker sends XCH to the maker
def take_cat_to_xch_offer(
    taker_offer: Offer, maker_request_payments: Program, partial_info: PartialInfo
):
    offer_asset_id = partial_info.offer_asset_id
    parent_inner_puzzle_hash = partial_info.to_partial_puzzle().get_tree_hash()

    sb = taker_offer.to_spend_bundle()
    taker_offer_coin_spends = sb.coin_spends

    # print(taker_offer.to_bech32())
    # print(json.dumps(sb.to_json_dict(), indent=2))

    # partial_taker coin spends & notarized payments
    coin_spends: Dict[str, CoinSpend] = {}  # offer input CAT coins
    notarized_payments_solutions: List[Any] = []  # request XCH payments
    settlement_coin_spends: List[CoinSpend] = []  # settlement coin spends (XCH)

    for cs in taker_offer_coin_spends:
        if cs.coin.parent_coin_info != ZERO_32:
            coin_name = cs.coin.name().hex()
            coin_spends[coin_name] = cs
        else:
            solutions = cs.solution.to_program().as_python()
            notarized_payments_solutions.append(solutions)

    for asset_id, coins in taker_offer.get_offered_coins().items():
        for coin in coins:
            parent_cs = coin_spends[coin.parent_coin_info.hex()]
            settlement_cs = make_spend(
                coin=parent_cs.coin,
                puzzle_reveal=OFFER_MOD,
                solution=Program.to([maker_request_payments]),
            )
            settlement_coin_spends.append(settlement_cs)

    taker_coin_spends = list(coin_spends.values()) + settlement_coin_spends

    return (
        taker_coin_spends,
        Program.to(notarized_payments_solutions[0]),
        sb.aggregated_signature,
    )


# taking xch offer
# taker sends CAT to the maker
def take_xch_to_cat_offer(taker_offer: Offer, maker_request_payments: Program):
    sb = taker_offer.to_spend_bundle()
    taker_offer_coin_spends = sb.coin_spends
    # partial_taker coin spends & notarized payments
    coin_spends: Dict[str, CoinSpend] = {}  # offer input CAT coins
    notarized_payments_solutions: List[Any] = []  # request XCH payments

    for cs in taker_offer_coin_spends:
        if cs.coin.parent_coin_info != ZERO_32:
            coin_name = cs.coin.name().hex()
            coin_spends[coin_name] = cs
        else:
            solutions = cs.solution.to_program().as_python()
            notarized_payments_solutions.append(solutions)

    settlement_spendable_cats: List[SpendableCAT] = []  # settlement spendable CAT
    for asset_id, coins in taker_offer.get_offered_coins().items():
        for coin in coins:
            parent_cs = coin_spends[coin.parent_coin_info.hex()]
            matched_cat_puzzle = match_cat_puzzle(
                uncurry_puzzle(parent_cs.puzzle_reveal.to_program())
            )

            if matched_cat_puzzle is None:
                # TODO: raise error?
                continue

            parent_inner_puzzle_hash = list(matched_cat_puzzle)[2].get_tree_hash()
            lineage_proof = LineageProof(
                parent_cs.coin.parent_coin_info,
                parent_inner_puzzle_hash,
                uint64(parent_cs.coin.amount),
            )

            spendable_cat = SpendableCAT(
                coin=coin,
                limitations_program_hash=asset_id,
                inner_puzzle=OFFER_MOD,
                inner_solution=[maker_request_payments],
                lineage_proof=lineage_proof,
            )
            settlement_spendable_cats.append(spendable_cat)

    settlement_coin_spends = unsigned_spend_bundle_for_spendable_cats(
        CAT_MOD, settlement_spendable_cats
    ).coin_spends

    taker_coin_spends = list(coin_spends.values()) + settlement_coin_spends

    return (
        taker_coin_spends,
        Program.to(notarized_payments_solutions[0]),
        sb.aggregated_signature,
    )


async def create_taker_offer(
    partial_info: PartialInfo,
    fingerprint: int,
    request_mojos_minus_fees: uint64,
    taker_offer_mojos: uint64,
    blockchain_fee_mojos: uint64,
) -> Offer:
    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):

        offer_asset_id = (
            "1"
            if partial_info.offer_asset_id == bytes(0)
            else bytes32(partial_info.offer_asset_id).hex()
        )

        request_asset_id = (
            "1"
            if partial_info.request_asset_id == bytes(0)
            else bytes32(partial_info.request_asset_id).hex()
        )
        offer_dict = {
            offer_asset_id: request_mojos_minus_fees,
            request_asset_id: -1 * taker_offer_mojos,
        }

        create_offer_res = await wallet_rpc_client.create_offer_for_ids(
            offer_dict=offer_dict,
            tx_config=DEFAULT_TX_CONFIG,
            validate_only=False,
            fee=blockchain_fee_mojos,
        )

        return create_offer_res.offer


async def take_partial_offer(
    taker_offer: Offer,
    create_offer_coin_sb: Optional[SpendBundle],
    partial_coin: Coin,
    partial_info: PartialInfo,
    request_mojos: uint64,
    fee_mojos: uint64,
    taker_offer_mojos: uint64,
    coin_spends: List[CoinSpend],
):
    # partial coin id (nonce) for puzzle announcement
    partial_coin_id = partial_coin.name()
    # only request the amount minus fees
    request_mojos_minus_fees = request_mojos - fee_mojos

    # create spend bundle
    p = partial_info.to_partial_puzzle()
    s = Program.to(
        [
            partial_coin.amount,
            partial_coin_id,
            partial_coin.puzzle_hash,
            request_mojos,
            0,
        ]
    )
    partial_ph = p.get_tree_hash()
    # print(f"partial_ph: {partial_ph}")
    # print(f"partial_coin: {partial_coin}")

    if partial_info.offer_asset_id == bytes(0) and partial_info.request_asset_id:

        maker_request_payments = Program.to(
            [
                partial_coin_id,
                [
                    partial_info.maker_puzzle_hash,
                    taker_offer_mojos,
                    [partial_info.maker_puzzle_hash],
                ],
            ]
        )
        (
            taker_coin_spends,
            taker_request_payments,
            taker_offer_sig,
        ) = take_xch_to_cat_offer(taker_offer, maker_request_payments)

        partial_cs: CoinSpend = make_spend(partial_coin, puzzle_reveal=p, solution=s)
        partial_offer_sb = SpendBundle(
            [
                partial_cs,
                make_spend(
                    Coin(
                        parent_coin_info=partial_coin.name(),
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

        next_offer = partial_info.get_next_partial_offer(partial_coin, request_mojos)
        return sb, next_offer
    elif partial_info.offer_asset_id and partial_info.request_asset_id == bytes(0):
        # prepare taker coin spends
        # - taker spends XCH to create settlement
        # - settlement is spent to maker

        # maker requests XCH
        # taker_offer_mojos = partial_info.get_output_mojos(request_mojos)
        maker_request_payments = Program.to(
            [
                partial_coin_id,
                [
                    partial_info.maker_puzzle_hash,
                    taker_offer_mojos,
                    [partial_info.maker_puzzle_hash],
                ],
            ]
        )
        (
            taker_coin_spends,
            taker_request_payments,
            taker_offer_sig,
        ) = take_cat_to_xch_offer(
            taker_offer, maker_request_payments, partial_info=partial_info
        )

        # prepare maker coin spends
        # - launcher CAT coin spend if exists
        # - partial CAT coin spend
        # - maker settlement CAT coin spend

        # parent can be either launcher or partial coin
        parent_cs = await get_partial_coin_parent_coin_spend(coin_spends, partial_coin)
        matched_cat_puzzle = match_cat_puzzle(
            uncurry_puzzle(parent_cs.puzzle_reveal.to_program())
        )

        if matched_cat_puzzle is None:
            raise Exception("Failed to match CAT puzzle")

        parent_inner_puzzle_hash = list(matched_cat_puzzle)[2].get_tree_hash()

        partial_sc = get_partial_spendable_cat(
            asset_id=partial_info.offer_asset_id,
            partial_coin=partial_coin,
            partial_puzzle=p,
            parent_coin=parent_cs.coin,
            parent_inner_puzzle_hash=parent_inner_puzzle_hash,
            partial_solution=s,
        )
        # print(partial_sc)

        partial_cs = unsigned_spend_bundle_for_spendable_cats(
            CAT_MOD, [partial_sc]
        ).coin_spends[0]

        # print(json.dumps(partial_cs.to_json_dict(), indent=2))

        cat_settlement_ph = CAT_MOD.curry(
            CAT_MOD.get_tree_hash(), partial_info.offer_asset_id, partial_ph
        ).get_tree_hash_precalc(partial_ph)

        # print(f"cat_settlement_ph: {cat_settlement_ph}")

        cat_settlement_coin = Coin(
            parent_coin_info=partial_coin.name(),
            puzzle_hash=cat_settlement_ph,
            amount=request_mojos_minus_fees,
        )
        # print(cat_settlement_coin)
        lineage_proof = LineageProof(
            partial_cs.coin.parent_coin_info,
            partial_ph,
            uint64(partial_cs.coin.amount),
        )

        cat_settlement_sc = SpendableCAT(
            coin=cat_settlement_coin,
            limitations_program_hash=partial_info.offer_asset_id,
            inner_puzzle=OFFER_MOD,
            inner_solution=taker_request_payments,
            lineage_proof=lineage_proof,
        )

        settlement_coin_spends = unsigned_spend_bundle_for_spendable_cats(
            CAT_MOD, [cat_settlement_sc]
        ).coin_spends
        # print(settlement_coin_spends)

        partial_offer_sb = SpendBundle(
            [
                partial_cs,
            ]
            + settlement_coin_spends
            + taker_coin_spends,
            taker_offer_sig,
        )

        sb = (
            SpendBundle.aggregate([create_offer_coin_sb, partial_offer_sb])
            if create_offer_coin_sb
            else partial_offer_sb
        )
        # print(json.dumps(sb.to_json_dict(), indent=2))

        raise Exception("Not implemented")
    elif partial_info.offer_asset_id and partial_info.request_asset_id:
        raise Exception("Not implemented")
    else:
        raise Exception("Invalid offer and request asset ids")


def get_offer_values(partial_info: PartialInfo, request_mojos: uint64):
    fee_mojos = FEE_MOD.run(Program.to([partial_info.fee_rate, request_mojos])).as_int()
    taker_offer_mojos = partial_info.get_output_mojos(request_mojos)
    return fee_mojos, taker_offer_mojos


async def take_cmd_async(
    create_offer_coin_sb: Optional[SpendBundle],
    partial_coin: Coin,
    partial_info: PartialInfo,
    fingerprint: int,
    request_mojos: uint64,
    fee_mojos: uint64,
    taker_offer_mojos: uint64,
    blockchain_fee_mojos: uint64,
    coin_spends: List[CoinSpend],
    taker_offer: Optional[Offer] = None,
):
    try:
        if taker_offer is None:
            taker_offer = await create_taker_offer(
                partial_info,
                fingerprint,
                request_mojos - fee_mojos,
                taker_offer_mojos,
                blockchain_fee_mojos,
            )
        if taker_offer is None:
            print("Failed to create taker offer")
            return

        sb, next_offer = await take_partial_offer(
            taker_offer=taker_offer,
            create_offer_coin_sb=create_offer_coin_sb,
            partial_coin=partial_coin,
            partial_info=partial_info,
            request_mojos=request_mojos,
            fee_mojos=fee_mojos,
            taker_offer_mojos=taker_offer_mojos,
            coin_spends=coin_spends,
        )

        async with get_wallet_client(wallet_rpc_port, fingerprint) as (
            wallet_rpc_client,
            fingerprint,
            config,
        ):
            await wallet_rpc_client.push_tx(sb)

        ret = {
            "spend_bundle": sb.to_json_dict(),
            "taker_offer": taker_offer.to_bech32(),
        }

        if next_offer is not None:
            ret["next_offer"] = next_offer.to_bech32()
        print(json.dumps(ret, indent=2))
    except Exception as e:
        print(f"Error: {e}")


async def confirm_take_offer(
    fingerprint: int,
    partial_info: PartialInfo,
    request_mojos,
    request_mojos_minus_fees,
    fee_mojos,
    taker_offer_mojos,
):
    print("")

    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):
        offer_wallet_id, offer_wallet_name, offer_unit = await get_wallet(
            wallet_rpc_client, partial_info.offer_asset_id
        )
        request_wallet_id, request_wallet_name, request_unit = await get_wallet(
            wallet_rpc_client, partial_info.request_asset_id
        )

        if (
            partial_info.offer_asset_id == bytes(0) and partial_info.request_asset_id
        ) or (
            partial_info.offer_asset_id and partial_info.request_asset_id == bytes(0)
        ):
            print(
                f" {get_amount_str(taker_offer_mojos, request_wallet_name, request_unit)} -> {get_amount_str(request_mojos, offer_wallet_name, offer_unit)}"
            )

            print(
                f" Sending {get_amount_str(taker_offer_mojos, request_wallet_name, request_unit)}"
            )
            print(
                f" Paying {get_amount_str(fee_mojos, offer_wallet_name, offer_unit)} in fees"
            )
            print(
                f" Receiving {get_amount_str(request_mojos_minus_fees, offer_wallet_name, offer_unit)}"
            )
        elif partial_info.offer_asset_id and partial_info.request_asset_id:
            print("Not implemented")
        else:
            print("Invalid offer and request asset ids")

    return Confirm.ask("\n Would you like to take this offer?")


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
    "-a",
    "--request-mojos",
    required=False,
    default=None,
    help="Request XCH amount in mojos",
    type=uint64,
)
@click.option(
    "-m",
    "--fee",
    "blockchain_fee_mojos",
    help="The blockchain fee to use when taking the partial offer, in mojos",
    default="0",
    show_default=True,
)
@click.argument("partial_offer_file", type=click.File("r"), required=True)
@click.pass_context
def take_cmd(
    ctx,
    fingerprint,
    taker_offer_file,
    request_mojos,
    blockchain_fee_mojos,
    partial_offer_file,
):
    if taker_offer_file is None and request_mojos is None:
        print("Either offer file or request mojos is required.")
        return

    offer_bech32 = partial_offer_file.read()
    offer: Offer = Offer.from_bech32(offer_bech32)
    sb: SpendBundle = offer.to_spend_bundle()

    partial_cs = get_partial_coin_spend(sb.coin_spends)
    if partial_cs is None:
        print("Partial offer is not valid")
        return

    partial_coin = partial_cs.coin

    is_partial_coin_spent = asyncio.run(is_coin_spent(partial_coin.name()))
    if is_partial_coin_spent:
        print("Partial offer is not valid")
        return

    partial_info = PartialInfo.from_coin_spend(partial_cs)
    if partial_info is None:
        print("Partial offer is not valid")
        return

    # calculate request amounts and fees
    if taker_offer_file is not None:
        raise Exception("Not implemented")
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
        taker_offer_mojos = partial_info.get_output_mojosuint64(request_mojos)
    else:
        if partial_coin.amount < request_mojos:
            print(
                f"Requested amount, {request_mojos} mojos is greater than the offer amount, {partial_coin.amount} mojos."
            )
            return

        fee_mojos, taker_offer_mojos = get_offer_values(partial_info, request_mojos)
        request_mojos_minus_fees = request_mojos - fee_mojos

    display_partial_info(partial_info, partial_coin, is_valid=not is_partial_coin_spent)

    is_confirmed = asyncio.run(
        confirm_take_offer(
            fingerprint,
            partial_info,
            request_mojos,
            request_mojos_minus_fees,
            fee_mojos,
            taker_offer_mojos,
        )
    )

    create_offer_coin_sb = asyncio.run(
        get_create_offer_coin_sb(sb.coin_spends, sb.aggregated_signature)
    )

    if not is_confirmed:
        return
    else:
        asyncio.run(
            take_cmd_async(
                create_offer_coin_sb=create_offer_coin_sb,
                partial_coin=partial_coin,
                partial_info=partial_info,
                fingerprint=fingerprint,
                request_mojos=request_mojos,
                fee_mojos=fee_mojos,
                taker_offer_mojos=taker_offer_mojos,
                blockchain_fee_mojos=blockchain_fee_mojos,
                taker_offer=taker_offer if taker_offer_file is not None else None,
                coin_spends=sb.coin_spends,
            )
        )
