import numpy as np
from models.black_scholes import BlackScholes
from tools.static_def import PayoffType


class Option:

    def __init__(self, F, K, T, sigma, payout=PayoffType.CALL):
        self.F = F
        self.K = K
        self.T = T
        self.sigma = sigma
        self.payout = payout

    def __eq__(self, other):
        if not isinstance(other, Option):
            return False
        return self.sigma == other.sigma and self.F == other.F and self.K == other.K and self.T == other.T \
               and self.payout == other.payout

    def model(self):
        return BlackScholes(self.T, self.F, self.K, self.sigma, self.payout)

    if __name__ == "__main__":
        from products.option import Option
        call_option = Option(100, 100, 0.01, 0.2, PayoffType.PUT)
        print(call_option.model().delta())
        print(call_option.payout)
