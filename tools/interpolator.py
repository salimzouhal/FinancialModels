import numpy as np


class Interpolator:

    def __init__(self, xs, ys, method):
        self.xs = xs
        self.ys = ys
        self.method = method

    def get_interpolate(self, x):
        if x < self.xs[0]:
            return self.ys[0]
        if x > self.xs[-1]:
            return self.ys[-1]
        else:
            return self.interpolate(x)

    def interpolate(self, x):
        return np.interp(x, self.xs, self.ys) if self.method == "linear" else NotImplemented

