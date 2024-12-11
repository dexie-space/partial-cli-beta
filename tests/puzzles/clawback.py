from typing import List


from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.util.ints import uint64
from chia.util.hash import std_hash
from chia.wallet.conditions import (
    AggSigMe,
    AssertMyAmount,
    CreateCoin,
    Condition,
    parse_conditions_non_consensus,
)
from chia_rs import G1Element
from clvm.casts import int_to_bytes

from partial_cli.config import FEE_PH, FEE_RATE, genesis_challenge
from partial_cli.types.partial_info import PartialInfo

MAKER_PH = bytes32([17] * 32)
pk_bytes = bytes.fromhex(
    "8049a7369adf936b3ad73c88fc6abd3d172d1ea1661f7d6597842152c2652966ac6a9b93653124cd93bd9a769a039275"
)
MAKER_PK = G1Element.from_bytes(pk_bytes)
OFFER_TAIL_HASH = bytes32.from_hexstr(
    "1b19cf566eb4e2bf9f563eac9b0263c1bd8b1007163da62436306699142fc71d"
)
REQUEST_TAIL_HASH = bytes32.from_hexstr(
    "657bdae0165c622f635374e539ef7e4632750ecc87541071478c21a7ba67096c"
)

offer_mojos = uint64(2e12)

request_cat_mojos = uint64(600e3)

ZERO_32 = bytes32([0] * 32)
ONE_32 = bytes32([1] * 32)

coin_id = ONE_32


def condition_exists(conditions: List[Condition], condition: Condition):
    for c in conditions:
        if type(c) is type(condition):
            if c.to_program() == condition.to_program():
                return True
    return False


class TestClawback:
    partial_puzzle = PartialInfo(
        fee_puzzle_hash=FEE_PH,
        fee_rate=FEE_RATE,
        maker_puzzle_hash=MAKER_PH,
        public_key=MAKER_PK,
        offer_asset_id=OFFER_TAIL_HASH,
        offer_mojos=uint64(1e12),
        request_asset_id=REQUEST_TAIL_HASH,
        request_mojos=uint64(100e3),
    ).to_partial_puzzle()

    def test_exact_clawback(self):
        coin_amount = offer_mojos
        solution = Program.to(
            [
                coin_amount,  # coin amount
                coin_id,  # coin id
                ZERO_32,  # puzzle hash
                0,  # taken_mojos_or_clawback
            ]
        )

        result = self.partial_puzzle.run(solution)
        conditions = parse_conditions_non_consensus(
            result.as_iter(), abstractions=False
        )

        assert condition_exists(conditions, AssertMyAmount(coin_amount))
        assert condition_exists(
            conditions,
            CreateCoin(puzzle_hash=MAKER_PH, amount=coin_amount, memos=[MAKER_PH]),
        )
        assert condition_exists(
            conditions,
            AggSigMe(
                MAKER_PK,
                msg=std_hash(int_to_bytes(coin_amount)),
                coin_id=coin_id,
                additional_data=genesis_challenge,
            ),
        )

    def test_clawback_more(self):
        coin_amount = offer_mojos
        clawback_amount = coin_amount + 1
        solution = Program.to(
            [
                clawback_amount,
                ZERO_32,  # coin id
                ZERO_32,  # puzzle hash
                0,  # taken_mojos_or_clawback
            ]
        )

        result = self.partial_puzzle.run(solution)
        conditions = parse_conditions_non_consensus(
            result.as_iter(), abstractions=False
        )

        # ASSERT_MY_AMOUNT fails on blockchain
        assert condition_exists(conditions, AssertMyAmount(clawback_amount))

    def test_clawback_less(self):
        coin_amount = offer_mojos
        clawback_amount = coin_amount - 1
        solution = Program.to(
            [
                clawback_amount,
                coin_id,  # coin id
                ZERO_32,  # puzzle hash
                0,  # taken_mojos_or_clawback
            ]
        )

        result = self.partial_puzzle.run(solution)
        conditions = parse_conditions_non_consensus(
            result.as_iter(), abstractions=False
        )

        # ASSERT_MY_AMOUNT fails on blockchain
        assert condition_exists(conditions, AssertMyAmount(clawback_amount))
