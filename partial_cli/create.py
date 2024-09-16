import asyncio
from decimal import Decimal
import json
import pathlib
import rich_click as click
from typing import Optional

from chia.cmds.cmds_util import get_wallet_client
from chia.cmds.units import units
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend, make_spend
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint64

import chia.wallet.conditions as conditions_lib
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
    help="A wallet id to offer and the amount to offer (formatted like wallet_id:amount). Support XCH only",
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


async def create_offer(
    fingerprint: int, offer: str, request: str, filepath: Optional[pathlib.Path]
):
    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):
        offer_wallet_id, offer_amount = tuple(offer.split(":")[0:2])
        request_wallet, request_amount = tuple(request.split(":")[0:2])

        # only offer XCH and request CAT for now
        assert offer_wallet_id == "1"
        assert request_wallet != "1"

        tail_hash = bytes32.from_hexstr(request_wallet)
        result = await wallet_rpc_client.cat_asset_id_to_name(tail_hash)
        if result is not None:
            request_wallet = result[1]
        else:
            request_wallet = "Unknown CAT"

        offer_mojos = uint64(abs(int(Decimal(offer_amount) * units["chia"])))

        request_cat_mojos = uint64(abs(int(Decimal(request_amount) * units["cat"])))

        rate = RATE_MOD.run(Program.to([offer_mojos, request_cat_mojos])).as_int()

        # create_offer_for_ids to lock coins
        offer_dict = {
            "1": -1 * offer_mojos,
            tail_hash.hex(): request_cat_mojos,
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
        partial_info = PartialInfo(
            fee_puzzle_hash=FEE_PH,
            fee_rate=FEE_RATE,
            maker_puzzle_hash=maker_ph,
            public_key=public_key,
            tail_hash=tail_hash,
            rate=rate,
        )

        partial_puzzle = partial_info.to_partial_puzzle()
        partial_ph = partial_puzzle.get_tree_hash()

        signed_txn_res = await wallet_rpc_client.create_signed_transactions(
            additions=[
                {
                    "puzzle_hash": partial_ph,
                    "amount": offer_mojos,
                }
            ],
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

        offer = Offer.from_spend_bundle(maker_sb)
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
