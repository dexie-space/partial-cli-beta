import rich_click as click

from chia.cmds.cmds_util import get_wallet_client
from chia.rpc.wallet_request_types import GetPrivateKey, GetPrivateKeyResponse
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
