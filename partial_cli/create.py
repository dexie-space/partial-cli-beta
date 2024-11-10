import asyncio
from decimal import Decimal
import json
import pathlib
import rich_click as click
from typing import Optional

from chia.cmds.cmds_util import get_wallet_client
from chia.cmds.units import units
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend, make_spend
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint64

import chia.wallet.conditions as conditions_lib
from chia.wallet.payment import Payment
from chia.wallet.puzzle_drivers import PuzzleInfo
from chia.wallet.trading.offer import ZERO_32, Offer
from chia.wallet.util.tx_config import DEFAULT_TX_CONFIG

from chia_rs import G2Element

from partial_cli.config import FEE_PH, FEE_RATE, wallet_rpc_port
from partial_cli.puzzles import RATE_MOD
from partial_cli.types.partial_info import PartialInfo
from partial_cli.utils.shared import get_public_key


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


def get_launcher_coin(
    sb: SpendBundle, partial_ph: bytes32, offer_mojos: uint64
) -> Coin:
    for cs in sb.coin_spends:
        result = cs.puzzle_reveal.to_program().run(cs.solution.to_program())
        conditions_list = conditions_lib.parse_conditions_non_consensus(
            result.as_iter(), abstractions=False
        )
        for c in conditions_list:
            if c == conditions_lib.CreateCoin(
                puzzle_hash=partial_ph, amount=offer_mojos
            ):
                return cs.coin
    return None


async def get_wallet_name(wallet_rpc_client: WalletRpcClient, asset_id: bytes32) -> str:
    wallet_name_res = await wallet_rpc_client.cat_asset_id_to_name(asset_id)
    if wallet_name_res is None:
        raise Exception(f"Unknown wallet or asset id: {asset_id.hex()}")
    return wallet_name_res[1]


async def create_offer(
    fingerprint: int, offer: str, request: str, filepath: Optional[pathlib.Path]
):
    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):
        offer_wallet, offer_amount = tuple(offer.split(":")[0:2])
        request_wallet, request_amount = tuple(request.split(":")[0:2])

        # can't offer and request same wallet
        assert offer_wallet != request_wallet

        offer_asset_id = (
            bytes(0)
            if offer_wallet == "1"
            else bytes(bytes32.from_hexstr(offer_wallet))
        )
        offer_wallet_name = (
            "XCH"
            if offer_asset_id == bytes(0)
            else await get_wallet_name(wallet_rpc_client, offer_asset_id)
        )
        offer_mojos = uint64(
            abs(
                int(
                    Decimal(offer_amount)
                    * (units["chia"] if offer_wallet_name == "XCH" else units["cat"])
                )
            )
        )

        request_asset_id = (
            bytes(0)
            if request_wallet == "1"
            else bytes(bytes32.from_hexstr(request_wallet))
        )

        request_wallet_name = (
            "XCH"
            if request_asset_id == bytes(0)
            else await get_wallet_name(wallet_rpc_client, request_asset_id)
        )
        request_mojos = uint64(
            abs(
                int(
                    Decimal(request_amount)
                    * (units["chia"] if request_wallet_name == "XCH" else units["cat"])
                )
            )
        )

        rate = RATE_MOD.run(
            Program.to([offer_asset_id, request_asset_id, offer_mojos, request_mojos])
        ).as_int()

        print(
            f"Offering {offer_amount} {offer_wallet_name} for {request_amount} {request_wallet_name} with rate {rate}"
        )

        # create_offer_for_ids to lock coins
        offer_dict = {
            offer_wallet: -1 * offer_mojos,
            request_wallet: request_mojos,
        }
        create_offer_res = await wallet_rpc_client.create_offer_for_ids(
            offer_dict=offer_dict, tx_config=DEFAULT_TX_CONFIG, validate_only=False
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

        maker_ph = coins[0].puzzle_hash

        public_key = await get_public_key(fingerprint)

        print(maker_ph)
        print(public_key)
        print(rate)

        partial_info = PartialInfo(
            fee_puzzle_hash=FEE_PH,
            fee_rate=FEE_RATE,
            maker_puzzle_hash=maker_ph,
            public_key=public_key,
            offer_asset_id=offer_asset_id,
            request_asset_id=request_asset_id,
            rate=rate,
        )

        partial_puzzle = partial_info.to_partial_puzzle()
        partial_ph = partial_puzzle.get_tree_hash()

        if offer_asset_id == bytes(0) and bytes32(request_asset_id):
            signed_txn_res = await wallet_rpc_client.create_signed_transactions(
                additions=[{"puzzle_hash": partial_ph, "amount": offer_mojos}],
                coins=coins,
                tx_config=DEFAULT_TX_CONFIG,
                wallet_id=1,
            )

            # find launcher coin
            sb = signed_txn_res.signed_tx.spend_bundle
            launcher_coin = get_launcher_coin(sb, partial_ph, offer_mojos)

            assert launcher_coin is not None

            partial_coin = Coin(launcher_coin.name(), partial_ph, offer_mojos)

            # eph partial coin spend
            partial_cs: CoinSpend = make_spend(
                coin=partial_coin,
                puzzle_reveal=partial_puzzle,
                solution=Program.to(["dexie_partial"]),
            )
            partial_sb = SpendBundle([partial_cs], G2Element())
            maker_sb: SpendBundle = SpendBundle.aggregate([sb, partial_sb])

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

            driver_dict = {
                bytes32(request_asset_id): PuzzleInfo(
                    {
                        "type": "CAT",
                        "tail": f"0x{request_asset_id.hex()}",
                    }
                )
            }

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

            ret = {"partial_info": PartialInfo.to_json_dict(partial_info)}
            ret["partial_coin"] = partial_coin.to_json_dict()
            ret["launcher_coin"] = launcher_coin.to_json_dict()
            ret["offer"] = offer_bech32
            print(json.dumps(ret, indent=2))
        else:
            raise Exception("Not implemented")
