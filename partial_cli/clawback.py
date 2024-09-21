import asyncio
import json
import rich_click as click

from chia.cmds.cmds_util import get_wallet_client
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend, make_spend
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from chia.util.ints import uint64
from chia.wallet.trading.offer import ZERO_32, Offer
from clvm.casts import int_to_bytes

from partial_cli.config import genesis_challenge, wallet_rpc_port
from partial_cli.puzzles import get_create_offer_coin_sb, get_partial_coin_spend
from partial_cli.types.partial_info import PartialInfo
from partial_cli.utils.rpc import is_coin_spent

from chia_rs import AugSchemeMPL, G1Element, PrivateKey


async def get_clawback_signature(
    fingerprint: int,
    partial_coin_name: bytes32,
    partial_pk: G1Element,
    coin_amount: uint64,
):
    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):

        private_key_res = await wallet_rpc_client.get_private_key(fingerprint)
        sk = PrivateKey.from_bytes(bytes.fromhex(private_key_res["sk"]))
        assert sk.get_g1() == partial_pk

        return AugSchemeMPL.sign(
            sk,
            std_hash(int_to_bytes(coin_amount)) + partial_coin_name + genesis_challenge,
        )


async def clawback_partial_offer(
    create_offer_coin_sb: SpendBundle,
    partial_coin: Coin,
    partial_info: PartialInfo,
    fingerprint: int,
    clawback_fee_mojos: uint64,
):
    # create spend bundle
    p = partial_info.to_partial_puzzle()
    s = Program.to([partial_coin.amount, ZERO_32, 0, clawback_fee_mojos])

    eph_partial_cs: CoinSpend = make_spend(partial_coin, puzzle_reveal=p, solution=s)

    cb_signature = await get_clawback_signature(
        fingerprint,
        partial_coin_name=partial_coin.name(),
        partial_pk=partial_info.public_key,
        coin_amount=partial_coin.amount,
    )

    paritial_offer_sb = SpendBundle([eph_partial_cs], cb_signature)

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
@click.option(
    "-m",
    "--fee",
    "clawback_fee_mojos",
    help="The blockchain fee to use when clawing back the partial offer, in mojos",
    default="0",
    show_default=True,
    type=uint64,
)
@click.argument("offer_file", type=click.File("r"))
@click.pass_context
def clawback_cmd(ctx, fingerprint, clawback_fee_mojos, offer_file):
    offer_bech32 = offer_file.read()
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

    create_offer_coin_sb = asyncio.run(
        get_create_offer_coin_sb(sb.coin_spends, sb.aggregated_signature)
    )
    asyncio.run(
        clawback_partial_offer(
            create_offer_coin_sb=create_offer_coin_sb,
            partial_coin=partial_coin,
            partial_info=partial_info,
            fingerprint=fingerprint,
            clawback_fee_mojos=clawback_fee_mojos,
        )
    )
