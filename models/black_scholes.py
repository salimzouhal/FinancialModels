import numpy as np
import tools.distributions as td
from tools.static_def import PayoffType


class BlackScholes:

    def __init__(self, T, S, K, r, sigma, payout, d=0):
        self.T = T
        self.S = S
        self.K = K
        self.sigma = sigma
        self.payout = payout
        self.d = d
        self.r = r

    def d1(self):
        return (np.log(self.S / self.K) + (self.r - self.d + self.sigma ** 2 / 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def d1_at_s(self, s):
        return (np.log(s / self.K) + (self.r - self.d + self.sigma ** 2 / 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)

    def d2_at_s(self, s):
        return self.d1_at_s(s) - self.sigma * np.sqrt(self.T)

    @property
    def payout_sign(self):
        return 1. if self.payout == PayoffType.CALL else -1.

    def price(self):
        d1 = self.d1()
        d2 = self.d2()
        payout = self.payout_sign
        return payout * (self.S * np.exp(-self.d * self.T) * td.N(payout * d1)
                         - self.K * np.exp(-self.r * self.T) * td.N(payout * d2))

    def delta(self):
        payout = self.payout_sign
        return payout * td.N(payout * self.d1())

    def delta_at_s(self, s):
        payout = self.payout_sign
        return payout * td.N(payout * self.d1_at_s(s))

    def gamma(self):
        return (td.n(self.d1()) * np.exp((self.d - self.r) * self.T))/(self.S * self.sigma * np.sqrt(self.T))

    def gamma_at_s(self, s):
        return (td.n(self.d1_at_s(s)) * np.exp((self.d - self.r) * self.T))/(s * self.sigma * np.sqrt(self.T))

    def vega(self):
        return self.S * np.exp((self.d - self.r) * self.T) * td.n(self.d1()) * np.sqrt(self.T)

    def vega_at_s(self, s):
        return s * np.exp((self.d - self.r) * self.T) * td.n(self.d1_at_s(s)) * np.sqrt(self.T)

    def theta(self):
        return -(self.S * np.exp((self.d - self.r) * self.T) * td.n(self.d1()) * self.sigma)/(2 * np.sqrt(self.T)) \
            - self.payout_sign * (self.d - self.r) * self.S * np.exp((self.d - self.r) * self.T) * td.N(self.payout_sign * self.d1()) \
            - self.payout * self.r * self.K * np.exp(- self.r * self.T) * td.N(self.payout * self.d2())

    def theta_at_s(self, s):
        return -(s * np.exp((self.d - self.r) * self.T) * td.n(self.d1_at_s(s)) * self.sigma) / (2 * np.sqrt(self.T)) \
            - self.payout_sign * (self.d - self.r) * s * np.exp((self.d - self.r) * self.T) * td.N(
                self.payout_sign * self.d1_at_s(s)) \
            - self.payout * self.r * self.K * np.exp(- self.r * self.T) * td.N(self.payout * self.d2_at_s(s))

    def rho(self):
        return self.T * self.K * np.exp(-self.r * self.T) * td.N(self.d2())

    def rho_at_s(self, s):
        return self.payout_sign * self.T * self.K * np.exp(-self.r * self.T) * td.N(self.payout_sign * self.d2_at_s(s))