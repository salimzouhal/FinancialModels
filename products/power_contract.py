import numpy as np
import tools.distributions as td
from tools.static_def import PayoffType


class PowerContract:
    def __init__(self, S, K, T, r, sigma, d, pow):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.d = d
        self.pow = pow

    def price(self):
        return (self.S / self.K) ** pow * np.exp(((self.d - self.sigma ** 2 / 2) * self.pow - self.r + 0.5 * self.pow ** 2 * self.sigma ** 2) * self.T)


class PowerOption:

    def __init__(self, S, K, T, r, sigma, d, pow, payout):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.d = d
        self.pow = pow
        self.payout = payout

    @property
    def d1(self):
        return (np.log(self.S / self.K ** (1 / self.pow)) + (self.d + (self.pow - 0.5) * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    @property
    def d2(self):
        return self.d1 - self.pow * self.sigma * np.sqrt(self.T)

    @property
    def payout_sign(self):
        return 1. if self.payout == PayoffType.CALL else -1.

    def price(self):
        I1 = self.S ** self.pow * np.exp(((self.pow - 1) * (self.r + 0.5 * self.pow * self.sigma ** 2) - self.pow * (self.r - self.d)) * self.T) * td.N(self.payout_sign * self.d1)
        I2 = self.K * np.exp(- self.r * self.T) * td.N(self.payout_sign * self.d2)
        return self.payout_sign * (I1 - I2)


class CappedPowerOption(PowerOption):
    def __init__(self, S, K, T, r, sigma, d, pow, payout, cap):
        super().__init__(S, K, T, r, sigma, d, pow, payout)
        self.cap = cap

    @property
    def d3(self):
        return (np.log(self.S / (self.K + self.cap) ** (1 / self.pow)) + (self.d + (self.pow - 0.5) * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    @property
    def d4(self):
        return self.d3 - self.pow * self.sigma * np.sqrt(self.T)

    def price(self):
        I1 = self.S ** self.pow * np.exp(((self.pow - 1) * (self.r + 0.5 * self.pow * self.sigma ** 2) - self.pow * (
                    self.r - self.d)) * self.T) * (td.N(self.payout_sign * self.d1) - td.N(self.payout_sign * self.d3))
        I2 = np.exp(- self.r * self.T) * (self.K * td.N(self.payout_sign * self.d2) - (self.K + self.payout_sign * self.cap) * td.N(self.payout_sign * self.d4))
        return self.payout_sign * (I1 - I2)


if __name__ == "__main__":
    call_option = PowerOption(10, 100, 0.5, 0.08, 0.3, 0.02, 2, PayoffType.CALL)
    capped_call_option = CappedPowerOption()
    print(call_option.price())
