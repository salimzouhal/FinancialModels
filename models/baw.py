import numpy as np
import tools.distributions as td
from tools.static_def import PayoffType
from models.black_scholes import BlackScholes
from scipy.optimize import fsolve


class BAW:

    def __init__(self, S, K, T, r, sigma, payout=PayoffType.CALL, d=0):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.payout = payout
        self.d = d

    def baw_to_bsm(self):
        return BlackScholes(self.T, self.S, self.K , self.r, self.sigma, self.payout, self.d)

    @property
    def payout_sign(self):
        return 1. if self.payout == PayoffType.CALL else -1.

    @property
    def N(self):
        return 2 * self.d / self.sigma ** 2

    @property
    def M(self):
        return 2 * self.r / self.sigma ** 2

    @property
    def k(self):
        return 1 - np.exp(-self.r * self.T)

    @property
    def q(self):
        return 0.5 * (- (self.N - 1) + self.payout_sign * np.sqrt((self.N - 1) ** 2 + 4 * self.M / self.k))

    def critical_spot(self):
        def objective_function(s):
            lhs = self.payout_sign * (s - self.K)
            european_bs = self.baw_to_bsm()
            rhs = european_bs.price()
            rhs += self.payout_sign * (s / self.q) * (1 - np.exp((self.d - self.r) * self.T)
                                                      * td.N(self.payout_sign * european_bs.d1_at_s(s)))
            return (lhs - rhs) ** 2

        s_inf = self.K / (1 - 2 * ((- (self.N - 1) + self.payout_sign * np.sqrt((self.N - 1) ** 2 + 4 * self.M)) ** (-1)))
        h = - self.payout_sign * (self.d * self.T + 2 * self.payout_sign * self.sigma * np.sqrt(self.T)) * (self.K / (self.payout_sign * (s_inf - self.K)))
        guess = s_inf + (self.K - s_inf) * np.exp(h)

        return fsolve(objective_function, guess)[0]

    @property
    def A(self):
        european_bs = self.baw_to_bsm()
        return self.payout_sign * self.critical_spot() / self.q \
            * (1 - np.exp((self.d - self.r) * self.T) * td.N(self.payout_sign * european_bs.d1_at_s(self.critical_spot())))

    def price(self):
        european_bs = self.baw_to_bsm()
        if self.payout_sign * self.S < self.payout_sign * self.critical_spot():
            return european_bs.price() + self.A * (self.S / self.critical_spot()) ** self.q
        else:
            return self.payout_sign * (self.S - self.K)


