from tools.static_def import PayoffType
from products.option import Option
from models.baw import BAW
import numpy as np
from products.american_option import AmericanOption


class AmericanPerpetualOption(AmericanOption):

    def __init__(self, S, K, T, r, sigma, payout=PayoffType.CALL, d=0):
        super().__init__(S, K, np.inf, r, sigma, payout, d)

    @property
    def payout_sign(self):
        return 1. if self.payout == PayoffType.CALL else -1.

    def price(self):
        y = 1/2 - self.d / self.sigma ** 2 + self.payout_sign * np.sqrt((self.d / self.sigma ** 2 - 1 / 2) ** 2 + 2 * self.r / self.sigma ** 2)
        price = (self.payout_sign * self.K / (y - 1)) * ((y - 1) / y * self.S / self.K) ** y
        return price


if __name__ == "__main__":
    call_option = AmericanPerpetualOption(100, 100, 10000, 0.01, 0.2, PayoffType.CALL)
    print(call_option.price())