from models.black_scholes import BlackScholes
from tools.static_def import PayoffType
import matplotlib.pyplot as plt
import numpy as np

class Option:

    def __init__(self, S, K, T, r, sigma, payout=PayoffType.CALL, d=0):
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.payout = payout
        self.d = d
        self.r = r

    def __eq__(self, other):
        if not isinstance(other, Option):
            return False
        return self.sigma == other.sigma and self.S == other.S and self.K == other.K and self.T == other.T \
               and self.payout == other.payout and self.d == other.d and self.r == other.r

    def model(self):
        return BlackScholes(self.T, self.S, self.K, self.r, self.sigma, self.payout, self.d)

    def price(self):
        return self.model().price()

    def price_at_spot(self, S):
        dummy_option = Option(S, self.K, self.T, self.r, self.sigma, self.payout, self.d)
        return dummy_option.price()

    def payoff(self, spot):
        return max(spot - self.K, 0) if self.payout == PayoffType.CALL else max(self.K - spot, 0)

    def plot(self):
        spots = np.linspace(1, 200, 100)
        payoffs = [self.payoff(spot) for spot in spots]
        plt.plot(spots, payoffs, 'r--', label='Payoff')
        prices = [self.price_at_spot(spot) for spot in spots]
        plt.plot(spots, prices, label='Price')
        plt.title('Option Payoff and Price')
        plt.xlabel('Underlying spot')
        plt.ylabel('Payoff')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    call_option = Option(100, 100, 2, 0.01, 0.2, PayoffType.PUT)
    print(call_option.model().delta())
    print(call_option.payout)
    call_option.plot()
