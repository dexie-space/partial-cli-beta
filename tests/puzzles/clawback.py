from typing import List

from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.util.ints import uint64
from chia.wallet.conditions import (
    AggSigMe,
    AssertMyAmount,
    Condition,
    parse_conditions_non_consensus,
)
from chia_rs import G1Element


from partial_cli.config import FEE_PH, FEE_RATE
from partial_cli.types.partial_info import PartialInfo
from partial_cli.puzzles import MOD, MOD_HASH, RATE_MOD

MAKER_PH = bytes32([17] * 32)
pk_bytes = bytes.fromhex(
    "8049a7369adf936b3ad73c88fc6abd3d172d1ea1661f7d6597842152c2652966ac6a9b93653124cd93bd9a769a039275"
)
MAKER_PK = G1Element.from_bytes(pk_bytes)
TAIL_HASH = bytes32.from_hexstr(
    "d82dd03f8a9ad2f84353cd953c4de6b21dbaaf7de3ba3f4ddd9abe31ecba80ad"
)
OFFER_MOJOS = uint64(2e12)

request_cat_mojos = uint64(600e3)
RATE = RATE_MOD.run(Program.to([OFFER_MOJOS, request_cat_mojos])).as_int()
ZERO_32 = bytes32([0] * 32)


def condition_exists(conditions: List[Condition], condition: Condition):
    for c in conditions:
        if type(c) is type(condition):
            if c.to_program() == condition.to_program():
                return True
    return False


class TestClawback:
    def test_clawback(self):
        partial_info = PartialInfo(
            fee_puzzle_hash=FEE_PH,
            fee_rate=FEE_RATE,
            maker_puzzle_hash=MAKER_PH,
            public_key=MAKER_PK,
            tail_hash=TAIL_HASH,
            rate=RATE,
            offer_mojos=OFFER_MOJOS,
        )
        partial_puzzle = partial_info.to_partial_puzzle()
        solution = Program.to(
            [
                ZERO_32,  # coin id
                0,  # taken_mojos_or_clawback
                0,  # chain_fee_mojos
            ]
        )

        result = partial_puzzle.run(solution)
        conditions = parse_conditions_non_consensus(
            result.as_iter(), abstractions=False
        )

        assert condition_exists(
            conditions,
            AggSigMe(
                MAKER_PK,
                msg=bytes32.from_hexstr(
                    "0xe3d492e066f7a659546588a7b9d7884601c7475329cf6ca3dfb23ef5d3e13821"
                ),
            ),
        )
