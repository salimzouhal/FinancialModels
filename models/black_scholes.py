import numpy as np
import tools.distributions as td


class BlackScholes:

    def __init__(self, T, F, K, sigma, payout):
        self.T = T
        self.F = F
        self.K = K
        self.sigma = sigma
        self.payout = payout

    def d1(self):
        return (np.log(self.F / self.K) + (self.sigma ** 2 * self.T) / 2) / (self.sigma * np.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)

    def price(self):
        d1 = self.d1()
        d2 = self.d2()
        return self.F * td.N(d1) - self.K * td.N(d2) if self.payout == 1 else 0

    def delta(self):
        return td.N(self.d1())





