from typing import List


from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.util.ints import uint16, uint64
from chia.util.hash import std_hash
from chia.wallet.conditions import (
    AssertMyCoinID,
    AssertMyAmount,
    AssertMyPuzzleHash,
    CreateCoin,
    CreatePuzzleAnnouncement,
    Condition,
    parse_conditions_non_consensus,
)
from chia.wallet.trading.offer import OFFER_MOD_HASH
from chia_rs import G1Element
from clvm.casts import int_to_bytes

from partial_cli.config import genesis_challenge
from partial_cli.puzzles import (
    FEE_MOD,
    REQ_MOJOS_MOD,
    get_standard_clawback_puzzle,
)
from partial_cli.types.partial_info import PartialInfo


def condition_exists(conditions: List[Condition], condition: Condition):
    for c in conditions:
        if type(c) is type(condition):
            if c.to_program() == condition.to_program():
                return True
    return False


MAKER_PH = std_hash(bytes32([17] * 32))
OFFER_TAIL_HASH = bytes(0)
REQUEST_TAIL_HASH = bytes32.from_hexstr(
    "657bdae0165c622f635374e539ef7e4632750ecc87541071478c21a7ba67096c"
)

OFFER_MOJOS = uint64(2e12)
REQUEST_MOJOS = uint64(600e3)

FEE_PH = bytes32.from_hexstr(
    "bc1f6e34fbc556d279b2e2187f2b7271df540926f21f74e26ba212c78a56b9b9"
)

FEE_RATE = uint16(100)

ZERO_32 = bytes32([0] * 32)
ONE_32 = bytes32([1] * 32)

coin_id = std_hash(ONE_32)


class TestPartialTake:
    partial_info = PartialInfo(
        fee_puzzle_hash=FEE_PH,
        fee_rate=FEE_RATE,
        maker_puzzle_hash=MAKER_PH,
        clawback_mod=Program.to(0),
        offer_asset_id=OFFER_TAIL_HASH,
        offer_mojos=OFFER_MOJOS,
        request_asset_id=REQUEST_TAIL_HASH,
        request_mojos=REQUEST_MOJOS,
    )

    req_mojos_puzzle = REQ_MOJOS_MOD.curry(OFFER_MOJOS, REQUEST_MOJOS)

    def test_request_mojos_of_1e12(self):
        coin_amount = uint64(2e12)
        taken_amount = uint64(0.7e12)
        p = self.partial_info.to_partial_puzzle()
        coin_ph = p.get_tree_hash()
        s = Program.to([coin_amount, coin_id, coin_ph, taken_amount])
        result = p.run(s)
        conditions = parse_conditions_non_consensus(
            result.as_iter(), abstractions=False
        )

        # (ASSERT_MY_AMOUNT  0x01d1a94a2000)
        assert condition_exists(conditions, AssertMyAmount(coin_amount))

        # (ASSERT_MY_COIN_ID  0x72cd6e8422c407fb6d098690f1130b7ded7ec2f7f5e1d30bd9d521f015363793)
        assert condition_exists(conditions, AssertMyCoinID(coin_id))

        # # (ASSERT_MY_PUZZLEHASH  0x07f64b877708fdc1b8e1f472e94a6a79797c6dac925190cca6879c4e60e80aa9)
        assert condition_exists(conditions, AssertMyPuzzleHash(coin_ph))

        # # assert announcement from taker settlement
        # (ASSERT_PUZZLE_ANNOUNCEMENT  0xd2d8bc6e388f8787ab9d7996c56545ec8cb7803ea7bda04990e6d3bee92dc387)
        expected_request_mojos = self.req_mojos_puzzle.run(
            [uint64(taken_amount)]
        ).as_int()
        assert expected_request_mojos == uint64(210e3)
        maker_request_payments = Program.to(
            [
                coin_id,
                [
                    MAKER_PH,
                    expected_request_mojos,
                    [MAKER_PH],
                ],
            ]
        )
        apa = CreatePuzzleAnnouncement(
            msg=maker_request_payments.get_tree_hash(),
            puzzle_hash=self.partial_info.get_request_settlement_hash(),
        ).corresponding_assertion()
        assert condition_exists(conditions, apa)

        # create settlement coin
        # (CREATE_COIN  0xcfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7 0x00a15a04d200 (0xcfbfdeed5c4ca2de3d0bf520b9cb4bb7743a359bd2e6a188d19ce7dffc21d3e7))
        fee = FEE_MOD.run([self.partial_info.fee_rate, taken_amount]).as_int()
        taken_amount_after_fee = taken_amount - fee
        assert condition_exists(
            conditions,
            CreateCoin(
                puzzle_hash=OFFER_MOD_HASH,
                amount=taken_amount_after_fee,
                memos=[OFFER_MOD_HASH],
            ),
        )

        # create fee coin
        # (CREATE_COIN  0xbc1f6e34fbc556d279b2e2187f2b7271df540926f21f74e26ba212c78a56b9b9 0x01a13b8600 (0xbc1f6e34fbc556d279b2e2187f2b7271df540926f21f74e26ba212c78a56b9b9))
        assert condition_exists(
            conditions,
            CreateCoin(
                puzzle_hash=FEE_PH,
                amount=fee,
                memos=[FEE_PH],
            ),
        )

        # create new partial coin
        # (CREATE_COIN  0x07f64b877708fdc1b8e1f472e94a6a79797c6dac925190cca6879c4e60e80aa9 0x012eae09c800 (0x07f64b877708fdc1b8e1f472e94a6a79797c6dac925190cca6879c4e60e80aa9))
        new_amount = coin_amount - taken_amount
        assert condition_exists(
            conditions,
            CreateCoin(
                puzzle_hash=coin_ph,
                amount=new_amount,
                memos=[coin_ph],
            ),
        )
