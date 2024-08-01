import asyncio
from decimal import Decimal
import json
import rich_click as click


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
from chia.wallet.trading.offer import OFFER_MOD, OFFER_MOD_HASH, Offer
from chia.wallet.util.tx_config import DEFAULT_COIN_SELECTION_CONFIG, DEFAULT_TX_CONFIG

from chia_rs import G1Element

from partial_cli.config import wallet_rpc_port
from partial_cli.puzzles.partial import (
    PartialInfo,
    get_partial_info,
    get_puzzle,
    process_taker_offer,
)
from partial_cli.utils.shared import (
    Bytes32ParamType,
    G1ElementParamType,
    get_cat_puzzle_hash,
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
    help="Rate in 1000 (e.g., 1 XCH for 128.68 CAT is 128680)",
    type=uint64,
)
@click.option(
    "-a",
    "--offer-mojos",
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
    offer_mojos: uint64,
    show_hash: bool,
):
    p = get_puzzle(puzzle_hash, public_key, tail_hash, rate, offer_mojos)
    print(rate, offer_mojos)
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
        result = await wallet_rpc_client.cat_asset_id_to_name(tail_hash)
        if result is not None:
            request_wallet = result[1]
        else:
            request_wallet = "Unknown CAT"

        offer_mojos = uint64(abs(int(Decimal(offer_amount) * units["chia"])))

        request_cat_mojos = uint64(abs(int(Decimal(request_amount) * units["cat"])))

        rate = uint64((request_cat_mojos / offer_mojos) * 1e12)
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

        partial_info = PartialInfo(
            maker_puzzle_hash=maker_puzzle_hash,
            public_key=public_key,
            tail_hash=tail_hash,
            rate=rate,
            offer_mojos=offer_mojos,
        )
        # print(partial_info)
        # print(partial_info.to_json_dict())

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
@click.option(
    "-a",
    "--taken_mojos",
    required=True,
    default=None,
    help="Taken amount in mojos",
    type=uint64,
)
@click.argument("offer_file", type=click.File("r"))
@click.pass_context
def take_cmd(ctx, fingerprint, taken_mojos, offer_file):
    # print(fingerprint, taken_mojos)

    offer_bech32 = offer_file.read()
    offer: Offer = Offer.from_bech32(offer_bech32)
    create_offer_coin_sb: SpendBundle = offer.to_spend_bundle()

    partial_coin, partial_info = get_partial_info(create_offer_coin_sb.coin_spends)
    if partial_info is None:
        print("No partial information found.")
        return

    # print(partial_coin.name().hex())
    # print(partial_info)

    # puzzle = get_puzzle(
    #     partial_info.maker_puzzle_hash,
    #     partial_info.public_key,
    #     partial_info.tail_hash,
    #     partial_info.rate,
    #     partial_info.offer_mojos,
    # )
    # print(puzzle.get_tree_hash().hex())

    asyncio.run(
        take_partial_offer(
            create_offer_coin_sb, partial_coin, partial_info, fingerprint, taken_mojos
        )
    )


async def create_taker_offer(
    partial_info: PartialInfo,
    fingerprint: int,
    taken_mojos: uint64,
):
    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_client,
        fingerprint,
        config,
    ):
        wallet_rpc_client: WalletRpcClient = wallet_client

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
    create_offer_coin_sb: SpendBundle,
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
    # partial_result_conditions = conditions_lib.parse_conditions_non_consensus(
    #     conditions=p.run(s).as_iter(), abstractions=False
    # )
    # print(partial_result_conditions)

    eph_partial_cs: CoinSpend = make_spend(partial_coin, puzzle_reveal=p, solution=s)

    # request cat mojos 32170
    # maker_cat_ph = get_cat_puzzle_hash(
    #     partial_info.tail_hash, partial_info.maker_puzzle_hash
    # )

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

    # print(eph_partial_cs)
    # print(maker_cat_ph.hex())
    # print(maker_request_payments)

    (
        taker_coin_spends,
        taker_request_payments,
        taker_offer_sig,
    ) = process_taker_offer(taker_offer, maker_request_payments)
    # print(len(taker_coin_spends))

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

    sb = SpendBundle.aggregate([create_offer_coin_sb, paritial_offer_sb])
    print(json.dumps(sb.to_json_dict(), indent=2))

    # async with get_wallet_client(wallet_rpc_port, fingerprint) as (
    #     wallet_client,
    #     fingerprint,
    #     config,
    # ):
    #     wallet_rpc_client: WalletRpcClient = wallet_client
    #     result = await wallet_rpc_client.push_tx(sb)
    #     print(result)
