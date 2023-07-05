from products.option import Option
import numpy as np
from tools.static_def import PayoffType
class ExecutiveStockOption(Option):
    def __init__(self, S, K, T, r, sigma, payout, d, lambda_):
        super().__init__(S, K, T, r, sigma, payout, d)
        self.lambda_ = lambda_

    def price(self):
        price = Option(self.S, self.K, self.T, self.r, self.sigma, self.payout, self.d).price()
        return np.exp(-self.lambda_ * self.T) * price


if __name__ == "__main__":
    call_option = ExecutiveStockOption(60, 64, 2, 0.07, 0.38, PayoffType.CALL, 0.03, 0.15)
    print(call_option.price())

