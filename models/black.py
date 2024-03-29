import numpy as np
import tools.distributions as td
from tools.static_def import PayoffType


class Black:

    def __init__(self, T, F, K, r, sigma, payout):
        self.T = T
        self.F = F
        self.K = K
        self.sigma = sigma
        self.payout = payout
        self.r = r

    def d1(self):
        return (np.log(self.F / self.K) + (self.sigma ** 2 / 2) * self.T) / (
                    self.sigma * np.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)

    def payout_sign(self):
        return 1. if self.payout == PayoffType.CALL else -1.

    def price(self):
        d1 = self.d1()
        d2 = self.d2()
        payout = self.payout_sign()
        return np.exp(-self.r * self.T) * payout * (
                    self.F * td.N(payout * d1) - self.K * td.N(payout * d2))

    def delta(self):
        payout = self.payout_sign()
        return payout * td.N(payout * self.d1())









