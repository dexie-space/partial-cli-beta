import json
import rich_click as click

from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.wallet.cat_wallet.cat_utils import CAT_MOD
import chia.wallet.conditions as conditions_lib

from chia_rs import G1Element


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


def get_cat_puzzle_hash(asset_id: bytes32, inner_puzzlehash: bytes32):
    if asset_id is None:
        return inner_puzzlehash

    outer_puzzlehash = CAT_MOD.curry(
        CAT_MOD.get_tree_hash(), asset_id, inner_puzzlehash
    ).get_tree_hash_precalc(inner_puzzlehash)
    return outer_puzzlehash


def get_partial_info(coin_spends):
    for cs in coin_spends:
        p = cs.puzzle_reveal.to_program()
        s = cs.solution.to_program()
        conditions = conditions_lib.parse_conditions_non_consensus(
            conditions=p.run(s).as_iter(), abstractions=False
        )
        for c in conditions:
            if type(c) is conditions_lib.CreateCoin:
                # check 1st memo
                if len(c.memos) == 2 and c.memos[0] == "dexie_partial".encode("utf-8"):
                    partial_info = json.loads(c.memos[1].decode("utf-8"))
                    return partial_info
    return None
