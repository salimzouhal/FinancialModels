from models.black_scholes import BlackScholes
from tools.static_def import PayoffType
import matplotlib.pyplot as plt
import numpy as np
from tools.gbm import GBM


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

    def delta(self):
        return self.model().delta()

    def mc_price(self, nb_sims=10000):
        gbm = GBM(self.S, self.T, self.r, self.sigma)
        payout = []
        for _ in range(0, nb_sims):
            s_maturity = gbm.generate_path()
            payout.append(self.payoff(s_maturity))
        return np.exp(-self.r * self.T) * np.mean(payout)

    def price_at_s(self, S):
        dummy_option = Option(S, self.K, self.T, self.r, self.sigma, self.payout, self.d)
        return dummy_option.price()

    def payoff(self, spot):
        return max(spot - self.K, 0) if self.payout == PayoffType.CALL else max(self.K - spot, 0)

    def payoff_plot(self):
        spots = np.linspace(1, 200, 100)
        payoffs = [self.payoff(spot) for spot in spots]
        plt.plot(spots, payoffs, 'r--', label='Payoff')
        prices = [self.price_at_s(spot) for spot in spots]
        plt.plot(spots, prices, label='Price')
        plt.title('Option Payoff and Price')
        plt.xlabel('Underlying spot')
        plt.ylabel('Payoff')
        plt.legend()
        plt.show()

    def delta_plot(self):
        spots = np.linspace(1, 200, 100)
        deltas = [self.model().delta_at_s(spot) for spot in spots]
        plt.plot(spots, deltas, 'r--', label='Delta')
        plt.title('Option delta')
        plt.xlabel('Underlying spot')
        plt.ylabel('Delta')
        plt.legend()
        plt.show()

    def vega_plot(self):
        spots = np.linspace(1, 200, 100)
        vegas = [self.model().vega_at_s(spot) for spot in spots]
        plt.plot(spots, vegas, 'r--', label='Vega')
        plt.title('Option vega')
        plt.xlabel('Underlying spot')
        plt.ylabel('Vega')
        plt.legend()
        plt.show()

    def gamma_plot(self):
        spots = np.linspace(1, 200, 100)
        gammas = [self.model().gamma_at_s(spot) for spot in spots]
        plt.plot(spots, gammas, 'r--', label='Gamma')
        plt.title('Option gamma')
        plt.xlabel('Underlying spot')
        plt.ylabel('Gamma')
        plt.legend()
        plt.show()

    def rho_plot(self):
        spots = np.linspace(1, 200, 100)
        rhos = [self.model().rho_at_s(spot) for spot in spots]
        plt.plot(spots, rhos, 'r--', label='Rho')
        plt.title('Option rho')
        plt.xlabel('Underlying spot')
        plt.ylabel('Rho')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    call_option = Option(100, 100, 2, 0.01, 0.2, PayoffType.PUT)
    print(call_option.model().delta())
    print(call_option.mc_price(nb_sims=100000))
    print(call_option.price())
    call_option.rho_plot()
