import numpy as np
import random


class GBM:
    def __init__(self, S0, T, r, sigma):
        self.S0 = S0
        self.T = T
        self.r = r
        self.sigma = sigma

    def generate_path(self):
        drift = (self.r - self.sigma ** 2 / 2) * self.T
        volatility = self.sigma * np.sqrt(self.T)
        return self.S0 * np.exp(drift + volatility * np.random.normal())



