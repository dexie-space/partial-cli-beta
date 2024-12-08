import asyncio
from decimal import Decimal
import pathlib
import rich_click as click
from typing import Optional

from chia.cmds.cmds_util import get_wallet_client
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend, make_spend
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint64

import chia.wallet.conditions as conditions_lib
from chia.wallet.cat_wallet.cat_utils import (
    CAT_MOD,
    get_innerpuzzle_from_puzzle,
    unsigned_spend_bundle_for_spendable_cats,
)
from chia.wallet.payment import Payment
from chia.wallet.puzzle_drivers import PuzzleInfo
from chia.wallet.trading.offer import ZERO_32, Offer

from chia_rs import G2Element

from partial_cli.config import FEE_PH, FEE_RATE, partial_tx_config, wallet_rpc_port
from partial_cli.puzzles import get_partial_coin_solution, get_partial_spendable_cat
from partial_cli.types.partial_info import PartialInfo
from partial_cli.utils.partial import display_partial_info
from partial_cli.utils.shared import get_public_key, get_puzzle_hash, get_wallet


# create
@click.command("create", help="create a partial offer requesting CAT token")
@click.option(
    "-f",
    "--fingerprint",
    required=True,
    help="Set the fingerprint to specify which wallet to use",
    type=int,
)
@click.option(
    "-o",
    "--offer",
    help="A wallet id to offer and the amount to offer (formatted like wallet_id:amount)",
    required=True,
)
@click.option(
    "-r",
    "--request",
    help="A wallet id of an asset to receive and the amount you wish to receive (formatted like wallet_id:amount). Support CAT only",
    required=True,
)
@click.option(
    "-p",
    "--filepath",
    help="The path to write the generated offer file to",
    required=False,
    type=click.Path(dir_okay=False, writable=True, path_type=pathlib.Path),
)
@click.pass_context
def create_cmd(
    ctx,
    fingerprint: int,
    offer: str,
    request: str,
    filepath: Optional[pathlib.Path],
):
    asyncio.run(create_offer(fingerprint, offer, request, filepath))


def get_launcher_coin_spend_from_launcher_coin_spends(
    launcher_coin_spends: SpendBundle,
    partial_ph: bytes32,
    offer_mojos: uint64,
) -> Optional[CoinSpend]:
    for cs in launcher_coin_spends.coin_spends:
        result = cs.puzzle_reveal.to_program().run(cs.solution.to_program())
        conditions_list = conditions_lib.parse_conditions_non_consensus(
            result.as_iter(), abstractions=False
        )
        for c in conditions_list:
            if type(c) is conditions_lib.CreateCoin:
                cc: conditions_lib.CreateCoin = c
                if (cc.puzzle_hash == partial_ph and cc.amount == offer_mojos) or (
                    cc.amount == offer_mojos and cc.memos == [partial_ph]
                ):
                    return cs
    return None


async def create_offer(
    fingerprint: int, offer: str, request: str, filepath: Optional[pathlib.Path]
):
    offer_wallet, offer_amount = tuple(offer.split(":")[0:2])
    request_wallet, request_amount = tuple(request.split(":")[0:2])
    assert offer_wallet != request_wallet

    driver_dict = {}

    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):
        offer_asset_id = (
            bytes(0)
            if offer_wallet == "1"
            else bytes(bytes32.from_hexstr(offer_wallet))
        )

        if offer_asset_id != bytes(0):
            driver_dict[bytes32(offer_asset_id)] = PuzzleInfo(
                {
                    "type": "CAT",
                    "tail": f"0x{offer_asset_id.hex()}",
                }
            )

        offer_wallet_id, offer_wallet_name, offer_unit = await get_wallet(
            wallet_rpc_client, offer_asset_id
        )
        offer_mojos = uint64(abs(int(Decimal(offer_amount) * offer_unit)))

        request_asset_id = (
            bytes(0)
            if request_wallet == "1"
            else bytes(bytes32.from_hexstr(request_wallet))
        )
        if request_asset_id != bytes(0):
            driver_dict[bytes32(request_asset_id)] = PuzzleInfo(
                {
                    "type": "CAT",
                    "tail": f"0x{request_asset_id.hex()}",
                }
            )

        request_wallet_id, request_wallet_name, request_unit = await get_wallet(
            wallet_rpc_client, request_asset_id
        )

        request_mojos = uint64(abs(int(Decimal(request_amount) * request_unit)))

        # create_offer_for_ids to lock coins
        offer_dict = {
            offer_wallet: -1 * offer_mojos,
            request_wallet: request_mojos,
        }
        create_offer_res = await wallet_rpc_client.create_offer_for_ids(
            offer_dict=offer_dict, tx_config=partial_tx_config, validate_only=False
        )

        offer = create_offer_res.offer
        if offer is None:
            raise Exception("Failed to create offer")

        # get coins from offer coin spends
        coins = [
            cs.coin
            for cs in offer.to_spend_bundle().coin_spends
            if cs.coin.parent_coin_info != ZERO_32
        ]

        maker_ph = await get_puzzle_hash(wallet_rpc_client, fingerprint)
        # print(coins[0].puzzle_hash.hex(), maker_ph.hex())

        public_key = await get_public_key(wallet_rpc_client, fingerprint)

        partial_info = PartialInfo(
            fee_puzzle_hash=FEE_PH,
            fee_rate=FEE_RATE,
            maker_puzzle_hash=maker_ph,
            public_key=public_key,
            offer_asset_id=offer_asset_id,
            offer_mojos=offer_mojos,
            request_asset_id=request_asset_id,
            request_mojos=request_mojos,
        )

        partial_puzzle = partial_info.to_partial_puzzle()
        partial_ph = partial_puzzle.get_tree_hash()

        signed_txn_res = await wallet_rpc_client.create_signed_transactions(
            additions=[{"puzzle_hash": partial_ph, "amount": offer_mojos}],
            coins=coins,
            tx_config=partial_tx_config,
            wallet_id=offer_wallet_id,
        )
        # find launcher coin
        sb = signed_txn_res.signed_tx.spend_bundle

        launcher_cs = get_launcher_coin_spend_from_launcher_coin_spends(
            sb, partial_ph, offer_mojos
        )

        assert launcher_cs is not None

        launcher_coin = launcher_cs.coin
        partial_coin_ph = (
            partial_ph
            if partial_info.offer_asset_id == bytes(0)
            else CAT_MOD.curry(
                CAT_MOD.get_tree_hash(), partial_info.offer_asset_id, partial_ph
            ).get_tree_hash_precalc(partial_ph)
        )

        partial_coin = Coin(launcher_coin.name(), partial_coin_ph, offer_mojos)
        print(partial_coin, partial_ph.hex())

        display_partial_info(
            partial_info,
            partial_coin,
            True,
            offer_wallet_name=offer_wallet_name,
            offer_unit=offer_unit,
            request_wallet_name=request_wallet_name,
            request_unit=request_unit,
            show_initial=False,
        )

        notarized_payments = None
        partial_cs = None
        if offer_asset_id == bytes(0) and bytes32(request_asset_id):
            # eph partial coin spend
            partial_cs: CoinSpend = make_spend(
                coin=partial_coin,
                puzzle_reveal=partial_puzzle,
                solution=get_partial_coin_solution(
                    partial_coin.amount, partial_coin.name()
                ),
            )

            notarized_payments = Offer.notarize_payments(
                {
                    bytes32(request_asset_id): [
                        Payment(
                            puzzle_hash=partial_info.maker_puzzle_hash,
                            amount=request_mojos,
                            memos=[partial_info.maker_puzzle_hash],
                        )
                    ]
                },
                coins=[partial_coin],
            )
        elif bytes32(offer_asset_id) and request_asset_id == bytes(0):
            launcher_inner_puzzle_hash = get_innerpuzzle_from_puzzle(
                launcher_cs.puzzle_reveal.to_program()
            ).get_tree_hash()

            # eph partial coin cat spend
            partial_sc = get_partial_spendable_cat(
                asset_id=offer_asset_id,
                partial_coin=partial_coin,
                partial_puzzle=partial_puzzle,
                parent_coin=launcher_coin,
                parent_inner_puzzle_hash=launcher_inner_puzzle_hash,
            )

            partial_cs = unsigned_spend_bundle_for_spendable_cats(
                CAT_MOD, [partial_sc]
            ).coin_spends[0]

            notarized_payments = Offer.notarize_payments(
                {
                    None: [
                        Payment(
                            puzzle_hash=partial_info.maker_puzzle_hash,
                            amount=request_mojos,
                            memos=[partial_info.maker_puzzle_hash],
                        )
                    ]
                },
                coins=[partial_coin],
            )
        elif bytes32(offer_asset_id) and bytes32(request_asset_id):

            raise Exception("Not implemented")
        else:
            raise Exception("Invalid asset id")
    partial_sb = SpendBundle([partial_cs], G2Element())
    maker_sb: SpendBundle = SpendBundle.aggregate([sb, partial_sb])

    # import json

    # print(json.dumps(sb.to_json_dict(), indent=2))
    # print(json.dumps(maker_sb.to_json_dict(), indent=2))
    # raise Exception("DEBUG")

    offer = Offer(
        notarized_payments,
        maker_sb,
        driver_dict,
    )
    offer_bech32 = offer.to_bech32()
    filepath = (
        filepath
        if filepath is not None
        else pathlib.Path.cwd() / f"launcher-{offer.name().hex()}.offer"
    )
    with filepath.open(mode="w") as file:
        file.write(offer_bech32)

    print(f"\nThe partial offer file is {filepath}")
