import asyncio
from decimal import Decimal
import rich_click as click

from chia.cmds.cmds_util import get_wallet_client
from chia.cmds.units import units
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint64

import chia.wallet.conditions as conditions_lib
from chia.wallet.trading.offer import Offer
from chia.wallet.util.tx_config import DEFAULT_COIN_SELECTION_CONFIG, DEFAULT_TX_CONFIG

from chia_rs import G1Element

from partial_cli.config import wallet_rpc_port

from partial_cli.puzzles.partial import PartialInfo


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
@click.pass_context
def create_cmd(
    ctx,
    fingerprint: int,
    offer: str,
    request: str,
):
    asyncio.run(create_offer(fingerprint, offer, request))


async def create_offer(fingerprint: int, offer: str, request: str):
    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_client,
        fingerprint,
        config,
    ):
        wallet_rpc_client: WalletRpcClient = wallet_client
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

        rate = uint64((request_cat_mojos / offer_mojos) * 1e12)

        # select coins
        coins = await wallet_rpc_client.select_coins(
            amount=offer_mojos,
            wallet_id=1,
            coin_selection_config=DEFAULT_COIN_SELECTION_CONFIG,
        )

        assert len(coins) == 1
        maker_coin = coins[0]
        maker_puzzle_hash = maker_coin.puzzle_hash

        # get public key
        private_key_res = await wallet_rpc_client.get_private_key(fingerprint)
        public_key = G1Element.from_bytes(bytes.fromhex(private_key_res["pk"]))
        partial_info = PartialInfo(
            maker_puzzle_hash=maker_puzzle_hash,
            public_key=public_key,
            tail_hash=tail_hash,
            rate=rate,
            offer_mojos=offer_mojos,
        )

        genesis_puzzle = partial_info.to_partial_puzzle()
        genesis_ph = genesis_puzzle.get_tree_hash()

        genesis_coin = Coin(maker_coin.name(), genesis_ph, offer_mojos)

        assert_genesis_coin_spend_announcement = [
            conditions_lib.AssertCoinAnnouncement(
                asserted_msg=maker_puzzle_hash, asserted_id=genesis_coin.name()
            )
        ]

        signed_txn_res = await wallet_rpc_client.create_signed_transaction(
            additions=[
                {
                    "puzzle_hash": genesis_ph,
                    "amount": offer_mojos,
                    "memos": partial_info.to_memos(),
                }
            ],
            coins=coins,
            tx_config=DEFAULT_TX_CONFIG,
            wallet_id=1,
            extra_conditions=assert_genesis_coin_spend_announcement,
        )

        maker_sb: SpendBundle = signed_txn_res.spend_bundle

        offer = Offer.from_spend_bundle(maker_sb)
        print(offer.to_bech32())
