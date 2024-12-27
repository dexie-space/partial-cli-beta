from decimal import Decimal
import rich_click as click
from typing import Tuple, Union

from chia.cmds.units import units
from chia.rpc.wallet_request_types import GetPrivateKey, GetPrivateKeyResponse
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.util.bech32m import decode_puzzle_hash
from chia.util.ints import uint8

from chia_rs import G1Element


class WalletAndAmountParamType(click.ParamType):
    name = "wallet_or_asset_id:amount"

    def convert(self, value, param, ctx):  # type: ignore
        try:
            wallet_str, amount_str = tuple(value.split(":")[0:2])

            amount = int(Decimal(amount_str))
            if amount < 0:
                self.fail(f"Amount must be positive: {amount_str}", param, ctx)

            if len(wallet_str) < 64:
                return uint8(wallet_str), amount
            else:
                return bytes(bytes32.from_hexstr(wallet_str)), amount
        except ValueError:
            self.fail(
                f"Invalid offer: {value} (wallet has to be either wallet_id or asset_id)",
                param,
                ctx,
            )


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


async def get_public_key(
    wallet_rpc_client: WalletRpcClient, fingerprint: int
) -> G1Element:
    private_key_res: GetPrivateKeyResponse = await wallet_rpc_client.get_private_key(
        GetPrivateKey(fingerprint)
    )
    return private_key_res.private_key.pk


async def get_puzzle_hash(wallet_rpc_client: WalletRpcClient, fingerprint: int):
    address = await wallet_rpc_client.get_next_address(1, False)
    return decode_puzzle_hash(address)


async def get_wallet(
    wallet_rpc_client: WalletRpcClient, wallet_or_asset_id: Union[uint8, bytes32]
) -> Tuple[int, str, int]:
    if type(wallet_or_asset_id) is uint8:
        if wallet_or_asset_id == 1:
            return 1, "XCH", bytes(0), units["chia"]
        else:
            asset_id = await wallet_rpc_client.get_cat_asset_id(wallet_or_asset_id)
            wallet_name = await wallet_rpc_client.get_cat_name(wallet_or_asset_id)
            return (
                wallet_or_asset_id,
                wallet_name,
                asset_id,
                units["cat"],
            )
    else:
        if wallet_or_asset_id == bytes(0):
            return 1, "XCH", bytes(0), units["chia"]

        wallet_res = await wallet_rpc_client.cat_asset_id_to_name(wallet_or_asset_id)
        if wallet_res is None:
            raise Exception(f"Unknown wallet or asset id: {wallet_or_asset_id.hex()}")

        wallet_id, wallet_name = wallet_res
        if wallet_id is None:
            raise Exception(f"Unknown wallet or asset id: {wallet_or_asset_id.hex()}")

        return wallet_id, wallet_name, wallet_or_asset_id, units["cat"]
