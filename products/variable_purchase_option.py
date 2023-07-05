from models.black_scholes import BlackScholes
import numpy as np
import tools.distributions as td


class VariablePurchaseOption:

    def __init__(self, S, K, T, r, sigma, L, U, disc, d=0.):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.L = L
        self.U = U
        self.d = d
        self.disc = disc

    @property
    def d1(self):
        return (np.log(self.S / self.U) + (self.d + self.sigma ** 2 / 2) * self.T) / (self.sigma * np.sqrt(self.T))

    @property
    def d3(self):
        return (np.log(self.S / self.L) + (self.d + self.sigma ** 2 / 2) * self.T) / (self.sigma * np.sqrt(self.T))

    @property
    def d5(self):
        return (np.log(self.S / (self.L * (1 - self.disc))) + (self.d + self.sigma ** 2 / 2) * self.T) / (self.sigma * np.sqrt(self.T))

    @property
    def d2(self):
        return self.d1 - self.sigma * np.sqrt(self.T)

    @property
    def d4(self):
        return self.d3 - self.sigma * np.sqrt(self.T)

    @property
    def d6(self):
        return self.d5 - self.sigma * np.sqrt(self.T)

    def price(self):
        N = lambda x : self.K / (x * (1 - self.disc))
        Nmin, Nmax = N(self.U), N(self.L)
        I1 = (self.K * self.disc) / (1 - self.disc) * np.exp(-self.r * self.T)
        I2 = Nmin * (self.S * np.exp((self.d - self.r) * self.T) * td.N(self.d1) - self.U * np.exp(-self.r * self.T) * td.N(self.d2))
        I3 = Nmax * (self.L * np.exp(- self.r * self.T) * td.N(-self.d4) - self.S * np.exp((self.d - self.r) * self.T) * td.N(-self.d3))
        I4 = Nmax * (self.L * (1 - self.disc) * np.exp(- self.r * self.T) * td.N(-self.d6) - self.S * np.exp((self.d - self.r) * self.T) * td.N(-self.d5))
        return I1 + I2 - I3 + I4


if __name__ == "__main__":
    call_option = VariablePurchaseOption(100, 101, 0.5, 0.05, 0.1, 101, 101, 0.2, 0.05)
    print(call_option.price())

