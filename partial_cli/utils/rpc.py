from chia.types.blockchain_format.sized_bytes import bytes32

from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.rpc.wallet_rpc_client import WalletRpcClient

from partial_cli.config import (
    self_hostname,
    full_node_rpc_port,
    chia_root,
    chia_config,
)


async def run_rpc(rpc_client, f, *args, **kwargs):
    try:
        result = await f(rpc_client, *args, **kwargs)
    except Exception as e:
        print("RPC call failed", e)
        return None
    finally:
        rpc_client.close()
        await rpc_client.await_closed()
    return result


def with_full_node_rpc_client(self_hostname, rpc_port, chia_root, chia_config):
    def _with_full_node_rpc_client(f):
        async def with_rpc_client(*args, **kwargs):
            rpc_client = await FullNodeRpcClient.create(
                self_hostname, rpc_port, chia_root, chia_config
            )
            return await run_rpc(rpc_client, f, *args, **kwargs)

        return with_rpc_client

    return _with_full_node_rpc_client


def with_wallet_rpc_client(self_hostname, rpc_port, chia_root, chia_config):
    def _with_wallet_rpc_client(f):
        async def with_rpc_client(*args, **kwargs):
            rpc_client = await WalletRpcClient.create(
                self_hostname, rpc_port, chia_root, chia_config
            )
            return await run_rpc(rpc_client, f, *args, **kwargs)

        return with_rpc_client

    return _with_wallet_rpc_client


async def fetch_rpc(client, rpc, request={}):
    response = await client.fetch(rpc, request)
    return response


def get_full_node_rpc(self_hostname, full_node_rpc_port, chia_root, chia_config):
    return with_full_node_rpc_client(
        self_hostname,
        full_node_rpc_port,
        chia_root,
        chia_config,
    )(fetch_rpc)


def get_wallet_rpc(self_hostname, wallet_rpc_port, chia_root, chia_config):
    return with_wallet_rpc_client(
        self_hostname,
        wallet_rpc_port,
        chia_root,
        chia_config,
    )(fetch_rpc)


@with_full_node_rpc_client(self_hostname, full_node_rpc_port, chia_root, chia_config)
async def is_coin_spent(full_node_rpc_client: FullNodeRpcClient, coin_name: bytes32):
    coin_record = await full_node_rpc_client.get_coin_record_by_name(coin_name)
    return coin_record is not None and coin_record.spent
