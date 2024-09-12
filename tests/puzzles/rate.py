from chia.util.ints import uint64
from partial_cli.puzzles import RATE_MOD


class TestRateCalculation:
    offer_xch_mojos_list = map(uint64, [1, 0.25e12, 1e12, 25e12])
    request_cat_mojos_list = map(uint64, [3, 75e3, 300e3, 7500e3])
    rates = [3000000000000, 300000, 300000, 300000]

    def test_good_inputs(self):
        for offer_xch_mojos, request_cat_mojos, rate in zip(
            self.offer_xch_mojos_list, self.request_cat_mojos_list, self.rates
        ):
            assert RATE_MOD.run([offer_xch_mojos, request_cat_mojos]).as_int() == rate
