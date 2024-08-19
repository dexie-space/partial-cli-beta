import asyncio
import json
import rich_click as click

from chia.cmds.cmds_util import get_wallet_client
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend, make_spend
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from chia.util.ints import uint64
from chia.wallet.trading.offer import ZERO_32, Offer
from clvm.casts import int_to_bytes

from partial_cli.config import wallet_rpc_port
from partial_cli.puzzles.partial import PartialInfo, get_partial_info, get_puzzle

from chia_rs import AugSchemeMPL, G1Element, PrivateKey


async def get_clawback_signature(
    fingerprint: int,
    partial_coin_name: bytes32,
    partial_pk: G1Element,
    offer_mojos: uint64,
):
    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):
        # TODO: get network constants from config
        # selected_network = config["wallet"]["selected_network"]
        genesis_challenge = bytes.fromhex(
            config["network_overrides"]["constants"]["mainnet"]["GENESIS_CHALLENGE"]
        )

        private_key_res = await wallet_rpc_client.get_private_key(fingerprint)
        sk = PrivateKey.from_bytes(bytes.fromhex(private_key_res["sk"]))

        assert sk.get_g1() == partial_pk

        return AugSchemeMPL.sign(
            sk,
            std_hash(int_to_bytes(offer_mojos)) + partial_coin_name + genesis_challenge,
        )


async def clawback_partial_offer(
    create_offer_coin_sb: SpendBundle,
    partial_coin: Coin,
    partial_info: PartialInfo,
    fingerprint: int,
):
    # create spend bundle
    p = get_puzzle(
        partial_info.maker_puzzle_hash,
        partial_info.public_key,
        partial_info.tail_hash,
        partial_info.rate,
        partial_info.offer_mojos,
    )
    s = Program.to([ZERO_32, 0])

    eph_partial_cs: CoinSpend = make_spend(partial_coin, puzzle_reveal=p, solution=s)

    cb_signature = await get_clawback_signature(
        fingerprint,
        partial_coin_name=partial_coin.name(),
        partial_pk=partial_info.public_key,
        offer_mojos=partial_info.offer_mojos,
    )

    paritial_offer_sb = SpendBundle([eph_partial_cs], cb_signature)

    # print(json.dumps(paritial_offer_sb.to_json_dict(), indent=2))
    # print(json.dumps(create_offer_coin_sb.to_json_dict(), indent=2))

    sb = (
        SpendBundle.aggregate([create_offer_coin_sb, paritial_offer_sb])
        if create_offer_coin_sb is not None
        else paritial_offer_sb
    )
    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):
        await wallet_rpc_client.push_tx(sb)
    print(json.dumps(sb.to_json_dict(), indent=2))


@click.command("clawback", help="clawback the partial offer coin.")
@click.option(
    "-f",
    "--fingerprint",
    required=True,
    help="Set the fingerprint to specify which wallet to use",
    type=int,
)
@click.argument("offer_file", type=click.File("r"))
@click.pass_context
def clawback_cmd(ctx, fingerprint, offer_file):
    offer_bech32 = offer_file.read()
    offer: Offer = Offer.from_bech32(offer_bech32)
    create_offer_coin_sb: SpendBundle = offer.to_spend_bundle()
    partial_coin, partial_info, is_genesis = get_partial_info(
        create_offer_coin_sb.coin_spends
    )
    if partial_info is None:
        print("No partial information found.")
        return

    asyncio.run(
        clawback_partial_offer(
            create_offer_coin_sb if is_genesis else None,
            partial_coin,
            partial_info,
            fingerprint,
        )
    )