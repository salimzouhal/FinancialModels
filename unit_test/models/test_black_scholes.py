import unittest
from products.option import Option
from tools.static_def import PayoffType


class TestBlackScholes(unittest.TestCase):

    def test_premium(self):
        self.nb_decimals = 4

        put_option = Option(100, 95, 0.5, 0.1, 0.2, PayoffType.PUT, 0.05)
        d1 = put_option.model().d1()
        d2 = put_option.model().d2()
        premium = put_option.price()
        self.assertAlmostEqual(d1, 0.6102, self.nb_decimals)
        self.assertAlmostEqual(d2, 0.4688, self.nb_decimals)
        self.assertAlmostEqual(premium, 2.4648, self.nb_decimals)

        ccy_option = Option(1.56, 1.6, 0.5, 0.06, 0.12, PayoffType.CALL, 0.08)
        d1 = ccy_option.model().d1()
        d2 = ccy_option.model().d2()
        premium = ccy_option.price()
        self.assertAlmostEqual(d1, -0.3738, self.nb_decimals)
        self.assertAlmostEqual(d2, -0.4587, self.nb_decimals)
        self.assertAlmostEqual(premium, 0.0291, self.nb_decimals)

