import numpy as np
from models.black_scholes import BlackScholes


class Option:

    def __init__(self, F, K, T, sigma, payout):
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
