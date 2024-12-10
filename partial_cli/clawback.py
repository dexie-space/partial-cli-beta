import asyncio
import json
import rich_click as click
from typing import Optional

from chia.cmds.cmds_util import get_wallet_client
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend, make_spend
from chia.types.spend_bundle import SpendBundle
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.util.hash import std_hash
from chia.util.ints import uint64
import chia.wallet.conditions as conditions_lib
from chia.wallet.trading.offer import ZERO_32, Offer
from clvm.casts import int_to_bytes

from partial_cli.config import genesis_challenge, partial_tx_config, wallet_rpc_port
from partial_cli.puzzles import get_create_offer_coin_sb, get_partial_coin_spend
from chia.rpc.wallet_request_types import GetPrivateKey, GetPrivateKeyResponse
from partial_cli.types.partial_info import PartialInfo
from partial_cli.utils.rpc import is_coin_spent

from chia_rs import AugSchemeMPL, G1Element, G2Element, PrivateKey


async def get_clawback_signature(
    wallet_rpc_client: WalletRpcClient,
    fingerprint: int,
    partial_coin_name: bytes32,
    partial_pk: G1Element,
    coin_amount: uint64,
) -> Optional[G2Element]:

    private_key_res: GetPrivateKeyResponse = await wallet_rpc_client.get_private_key(
        GetPrivateKey(fingerprint)
    )
    sk: PrivateKey = private_key_res.private_key.sk

    if sk.get_g1() != partial_pk:
        return None

    return AugSchemeMPL.sign(
        sk,
        std_hash(int_to_bytes(coin_amount)) + partial_coin_name + genesis_challenge,
    )


async def get_clawback_fee_spend_bundle(
    wallet_rpc_client: WalletRpcClient,
    clawback_fee_mojos: uint64,
    partial_coin_name: bytes32,
    maker_puzzle_hash: bytes32,
):
    coins = await wallet_rpc_client.select_coins(
        amount=clawback_fee_mojos,
        wallet_id=1,
        coin_selection_config=partial_tx_config.coin_selection_config,
    )

    if len(coins) == 0:
        raise Exception("Not enough coins to pay the clawback fee")

    total_amount = sum([coin.amount for coin in coins])
    fee_txn_res = await wallet_rpc_client.create_signed_transactions(
        additions=[
            {
                "puzzle_hash": maker_puzzle_hash,
                "amount": total_amount - clawback_fee_mojos,
            }
        ],
        coins=coins,
        extra_conditions=[conditions_lib.AssertConcurrentSpend(partial_coin_name)],
        fee=clawback_fee_mojos,
        tx_config=partial_tx_config,
        wallet_id=1,
    )

    return fee_txn_res.signed_tx.spend_bundle


async def clawback_cat_partial_offer(
    create_offer_coin_sb: SpendBundle,
    partial_coin: Coin,
    partial_info: PartialInfo,
    fingerprint: int,
    clawback_fee_mojos: uint64,
):
    # TODO: spendable cat
    pass


async def clawback_partial_offer(
    create_offer_coin_sb: SpendBundle,
    partial_coin: Coin,
    partial_info: PartialInfo,
    fingerprint: int,
    clawback_fee_mojos: uint64,
):
    # create spend bundle
    p = partial_info.to_partial_puzzle()
    s = Program.to([partial_coin.amount, ZERO_32, ZERO_32, 0])

    eph_partial_cs: CoinSpend = make_spend(partial_coin, puzzle_reveal=p, solution=s)

    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):

        cb_signature = await get_clawback_signature(
            wallet_rpc_client=wallet_rpc_client,
            fingerprint=fingerprint,
            partial_coin_name=partial_coin.name(),
            partial_pk=partial_info.public_key,
            coin_amount=partial_coin.amount,
        )
        if cb_signature is None:
            print(
                f"Failed to get clawback signature for public key {bytes(partial_info.public_key).hex()}"
            )
            return

        paritial_offer_sb = SpendBundle([eph_partial_cs], cb_signature)

        # blockchain fee
        fee_sb = (
            None
            if clawback_fee_mojos <= 0
            else await get_clawback_fee_spend_bundle(
                wallet_rpc_client=wallet_rpc_client,
                clawback_fee_mojos=clawback_fee_mojos,
                partial_coin_name=partial_coin.name(),
                maker_puzzle_hash=partial_info.maker_puzzle_hash,
            )
        )

        sb = SpendBundle.aggregate(
            list(
                filter(
                    lambda sb: sb is not None,
                    [create_offer_coin_sb, paritial_offer_sb, fee_sb],
                )
            )
        )

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
