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

    def PV(self, x, T, r, method="Linear"):
        if method == "Linear":
            return x/(1 + r * T)
        elif method == "Compound":
            return x/(1 + r)**T
        else:
            return x * np.exp(- r * T)

    def get_rates(self):
        return [self.zc_curve.get_value(date) for date in self.coupon_dates]

    def get_price(self):
        zc_rates = self.get_rates()
        return self.PV(self.fv, self.coupon_dates[-1], zc_rates[-1], self.method) + \
                sum([self.PV(self.cpn, date, rate, self.method) for rate, date in zip(zc_rates, self.coupon_dates)])

    def get_ytm(self):
        price = self.get_price()

        def difference(ytm):
            return ((self.PV(self.fv, self.coupon_dates[-1], ytm, self.method) + \
                sum([self.PV(self.cpn, date, ytm, self.method) for date in self.coupon_dates])) - price)**2

        zc_rates = self.get_rates()
        optimized = optimize.minimize(difference, np.array([zc_rates[0]]), bounds=optimize.Bounds([PRECISION], [np.inf]))
        return max(optimized.x[0], PRECISION)

    def get_duration(self):
        self.zc_curve.parallel_bump(BUMP)
        price_up = self.get_price()
        self.zc_curve.parallel_bump(-2 * BUMP)
        price_down = self.get_price()
        return (price_down - price_up) / BUMP


if __name__ == "__main__":
    pillars = [1., 2., 3., 4., 5., 6., 7., 8., 9., 10.]
    rates = 0.01 * pillars
    curve = Curve(pillars, rates, "linear")
    bond = Bond(5., 100., [1, 2, 3, 3.5, 4, 5], curve)
    print(bond.get_price())
    print(bond.get_ytm())
    print(bond.get_duration())










