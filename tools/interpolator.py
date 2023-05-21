import numpy as np


class Interpolator:

    def __init__(self, xs, ys, method="linear"):
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
        if self.method == "linear":
            return np.interp(x, self.xs, self.ys)
        else:
            return NotImplemented




