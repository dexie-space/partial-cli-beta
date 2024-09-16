from chia.util.ints import uint16, uint64

from partial_cli.puzzles import FEE_MOD


class TestFeeCalculation:
    fee_rates = list(map(lambda v: uint16(v * 100), [0, 0.1, 1, 10]))
    taken_xch_mojos_list = list(map(uint64, [1, 0.25e12, 1e12, 25e12]))
    fees = [
        list(map(uint64, [0, 0, 0, 0])),  # 0%
        list(map(uint64, [0, 25e7, 0.001e12, 0.025e12])),  # 0.1%
        list(map(uint64, [0, 25e8, 0.01e12, 0.25e12])),  # 1%
        list(map(uint64, [0, 25e9, 0.1e12, 2.5e12])),  # 10%
    ]

    def test_good_inputs(self):
        for fee_rate, fees in zip(self.fee_rates, self.fees):
            for i, taken_xch_mojos in enumerate(self.taken_xch_mojos_list):
                assert FEE_MOD.run([fee_rate, taken_xch_mojos]).as_int() == fees[i]
