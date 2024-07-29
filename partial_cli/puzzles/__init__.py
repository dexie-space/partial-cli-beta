import asyncio
from decimal import Decimal
import json
import rich_click as click


from chia.cmds.cmds_util import get_wallet_client
from chia.cmds.units import units
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.wallet.trading.offer import Offer
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint64
from chia.wallet.util.tx_config import DEFAULT_COIN_SELECTION_CONFIG, DEFAULT_TX_CONFIG

from chia_rs import G1Element

from partial_cli.config import wallet_rpc_port
from partial_cli.puzzles.partial import get_puzzle
from partial_cli.utils.shared import (
    Bytes32ParamType,
    G1ElementParamType,
    get_partial_info,
)


@click.command("get", help="get a serialized curried puzzle")
@click.option(
    "-ph",
    "--puzzle-hash",
    required=True,
    default=None,
    help="puzzle hash",
    type=Bytes32ParamType(),
)
@click.option(
    "-pk",
    "--public-key",
    required=True,
    default=None,
    help="public key",
    type=G1ElementParamType(),
)
@click.option(
    "-t",
    "--tail-hash",
    required=True,
    default=None,
    help="CAT tail hash",
    type=Bytes32ParamType(),
)
@click.option(
    "-r",
    "--rate",
    required=True,
    default=None,
    help="Rate (e.g., how many CAT token per XCH)",
    type=float,
)
@click.option(
    "-a",
    "--offer-amount",
    required=True,
    default=None,
    help="Offer amount in mojos",
    type=uint64,
)
@click.option(
    "-h",
    "--hash",
    "show_hash",
    required=False,
    is_flag=True,
    show_default=True,
    default=False,
    help="Show puzzle hash",
)
@click.pass_context
def get_cmd(
    ctx,
    puzzle_hash: bytes32,
    public_key: G1Element,
    tail_hash: bytes32,
    rate: uint64,
    offer_amount: uint64,
    show_hash: bool,
):
    p = get_puzzle(puzzle_hash, public_key, tail_hash, rate, offer_amount)
    if show_hash:
        print(p.get_tree_hash())
    else:
        print(str(p))


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
    "-pk",
    "--public-key",
    required=True,
    default=None,
    help="public key",
    type=G1ElementParamType(),
)
@click.pass_context
def create_cmd(
    ctx,
    fingerprint: int,
    offer: str,
    request: str,
    public_key: G1Element,
):
    asyncio.run(create_offer(fingerprint, offer, request, public_key))


async def create_offer(
    fingerprint: int, offer: str, request: str, public_key: G1Element
):
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
        result = await wallet_client.cat_asset_id_to_name(tail_hash)
        if result is not None:
            request_wallet = result[1]
        else:
            request_wallet = "Unknown CAT"

        offer_mojos = uint64(abs(int(Decimal(offer_amount) * units["chia"])))

        request_cat_mojos = uint64(abs(int(Decimal(request_amount) * units["cat"])))

        rate = (request_cat_mojos / offer_mojos) * 1e9
        # print(rate, request_cat_mojos, offer_mojos)

        # select coins
        coins = await wallet_rpc_client.select_coins(
            amount=offer_mojos,
            wallet_id=1,
            coin_selection_config=DEFAULT_COIN_SELECTION_CONFIG,
        )

        assert len(coins) == 1
        maker_coin = coins[0]
        maker_puzzle_hash = maker_coin.puzzle_hash

        genesis_puzzle = get_puzzle(
            maker_puzzle_hash, public_key, tail_hash, rate, offer_mojos
        )
        genesis_ph = genesis_puzzle.get_tree_hash()

        memos = {
            "maker_puzzle_hash": maker_puzzle_hash.hex(),
            "public_key": str(public_key),
            "tail_hash": tail_hash.hex(),
            "rate": rate,
            "offer_mojos": offer_mojos,
        }

        signed_txn_res = await wallet_rpc_client.create_signed_transaction(
            additions=[
                {
                    "puzzle_hash": genesis_ph,
                    "amount": 1e12,
                    "memos": ["dexie_partial", json.dumps(memos)],
                }
            ],
            coins=coins,
            tx_config=DEFAULT_TX_CONFIG,
            wallet_id=1,
        )

        maker_sb: SpendBundle = signed_txn_res.spend_bundle

        offer = Offer.from_spend_bundle(maker_sb)
        print(offer.to_bech32())


@click.command("take", help="Take the dexie partial offer.")
@click.option(
    "-f",
    "--fingerprint",
    required=True,
    help="Set the fingerprint to specify which wallet to use",
    type=int,
)
@click.argument("offer_file", type=click.File("r"))
@click.pass_context
def take_cmd(ctx, fingerprint, offer_file):
    offer_bech32 = offer_file.read()
    offer: Offer = Offer.from_bech32(offer_bech32)
    sb = offer.to_spend_bundle()

    partial_info = get_partial_info(sb.coin_spends)
    if partial_info is None:
        print("No partial information found.")
        return
    else:
        print(json.dumps(partial_info, indent=2))
