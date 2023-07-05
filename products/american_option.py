from tools.static_def import PayoffType
from products.option import Option
from models.baw import BAW


class AmericanOption:

    def __init__(self, S, K, T, r, sigma, payout=PayoffType.CALL, d=0):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.payout = payout
        self.d = d

    def __eq__(self, other):
        if not isinstance(other, Option):
            return False
        return self.sigma == other.sigma and self.S == other.S and self.K == other.K and self.T == other.T \
            and self.payout == other.payout and self.d == other.d and self.r == other.r

    def model(self):
        return BAW(self.S, self.K, self.T, self.r, self.sigma, self.payout, self.d)

    def price(self):
        return self.model().price()


if __name__ == "__main__":
    call_option = AmericanOption(100, 100, 50, 0.01, 0.2, PayoffType.CALL)
    print(call_option.price())
    print(call_option.model().critical_spot())




