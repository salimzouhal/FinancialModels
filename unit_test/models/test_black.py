import unittest
from products.option_on_futures import OptionOnFutures
from tools.static_def import PayoffType


class TestBlack(unittest.TestCase):

    def test_premium(self):
        self.nb_decimals = 4

        put_option = OptionOnFutures(19, 19, 0.75, 0.1, 0.28, PayoffType.PUT)
        d1 = put_option.model().d1()
        d2 = put_option.model().d2()
        premium = put_option.price()
        self.assertAlmostEqual(d1, 0.1212, self.nb_decimals)
        self.assertAlmostEqual(d2, -0.1212, self.nb_decimals)
        self.assertAlmostEqual(premium, 1.7011, self.nb_decimals)
