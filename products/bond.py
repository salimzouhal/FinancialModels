import numpy as np
from market.curve import Curve
from scipy import optimize

PRECISION = 1.e-5
BUMP = 1.e-6


class Bond:

    def __init__(self, cpn, fv, coupon_dates, zc_curve, method="Linear"):
        self.cpn = cpn
        self.fv = fv
        self.coupon_dates = coupon_dates
        self.zc_curve = zc_curve
        self.method = method

    def present_value(self, x, T, r, method="Linear"):
        if method == "Linear":
            return x/(1 + r * T)
        elif method == "Compound":
            return x/(1 + r)**T
        else:
            return x * np.exp(- r * T)

    def rates(self):
        return [self.zc_curve.get_value(date) for date in self.coupon_dates]

    def price(self):
        zc_rates = self.rates()
        return self.present_value(self.fv, self.coupon_dates[-1], zc_rates[-1], self.method) + \
                sum([self.present_value(self.cpn, date, rate, self.method) for rate, date in zip(zc_rates, self.coupon_dates)])

    def ytm(self):
        price = self.price()

        def difference(ytm):
            return ((self.present_value(self.fv, self.coupon_dates[-1], ytm, self.method) +
                     sum([self.present_value(self.cpn, date, ytm, self.method) for date in self.coupon_dates])) - price)**2

        zc_rates = self.rates()
        optimized = optimize.minimize(difference, np.array([zc_rates[0]]), bounds=optimize.Bounds([PRECISION], [np.inf]))
        return max(optimized.x[0], PRECISION)

    def duration(self):
        price = self.price()
        self.zc_curve.parallel_bump(BUMP)
        price_up = self.price()
        self.zc_curve.parallel_bump(-2 * BUMP)
        price_down = self.price()
        return (price_down - price_up) / (2 * BUMP * price)

    def macaulay_duration(self):
        return self.duration()/(1 + self.ytm())

    def convexity(self):
        price = self.price()
        self.zc_curve.parallel_bump(BUMP)
        price_up = self.price()
        self.zc_curve.parallel_bump(-2 * BUMP)
        price_down = self.price()
        return (price_down + price_up - 2 * price) / (2 * BUMP**2 * price)


if __name__ == "__main__":
    rates = [0.01 * x for x in range(1, 11)]
    pillars = [x for x in range(1, 11)]
    curve = Curve(pillars, rates, "linear")
    bond = Bond(5., 100., [1, 2, 3, 3.5, 4, 5], curve)
    print(bond.price())
    print(bond.ytm())
    print(bond.duration())
    print(bond.convexity())










