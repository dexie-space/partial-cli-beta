import rich_click as click
from typing import Tuple

from chia.cmds.cmds_util import get_wallet_client
from chia.cmds.units import units
from chia.rpc.wallet_request_types import GetPrivateKey, GetPrivateKeyResponse
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32

from chia_rs import G1Element
from partial_cli.config import wallet_rpc_port


class Bytes32ParamType(click.ParamType):
    name = "bytes32"

    def convert(self, value, param, ctx):  # type: ignore
        try:
            bytes32_value: bytes32 = bytes32.from_hexstr(value)
            return bytes32_value
        except ValueError:
            self.fail(f"Invalid bytes32: {value}", param, ctx)


class G1ElementParamType(click.ParamType):
    name = "G1Element"

    def convert(self, value, param, ctx):  # type: ignore
        try:
            pk: G1Element = G1Element.from_bytes(bytes.fromhex(value.replace("0x", "")))
            return pk
        except ValueError:
            self.fail(f"Invalid Public Key (G1Element): {value}", param, ctx)


class ProgramParamType(click.ParamType):
    name = "Program"

    def convert(self, value, param, ctx):  # type: ignore
        try:
            program = Program.fromhex(value)
            return program
        except ValueError:
            self.fail(f"Invalid Program: {value}", param, ctx)


async def get_public_key(fingerprint: int):
    async with get_wallet_client(wallet_rpc_port, fingerprint) as (
        wallet_rpc_client,
        fingerprint,
        config,
    ):
        private_key_res: GetPrivateKeyResponse = (
            await wallet_rpc_client.get_private_key(GetPrivateKey(fingerprint))
        )
        public_key = private_key_res.private_key.pk
        return public_key


async def get_wallet(
    wallet_rpc_client: WalletRpcClient, asset_id: bytes
) -> Tuple[int, str, int]:
    if asset_id == bytes(0):
        return 1, "XCH", units["chia"]
    else:
        wallet_res = await wallet_rpc_client.cat_asset_id_to_name(bytes32(asset_id))
        if wallet_res is None:
            raise Exception(f"Unknown wallet or asset id: {asset_id.hex()}")

        wallet_id, wallet_name = wallet_res
        if wallet_id is None:
            raise Exception(f"Unknown wallet or asset id: {asset_id.hex()}")
        return wallet_id, wallet_name, units["cat"]
