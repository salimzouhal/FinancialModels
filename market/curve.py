from tools.interpolator import Interpolator
import numpy as np

class Curve:

    def __init__(self, pillars, values, convention):
        self.pillars = pillars
        self.values = values
        self.convention = convention

    def get_value(self, pillar):
        if pillar in self.pillars:
            return self.values[self.pillars.index(pillar)]
        else:
            interpolator = Interpolator(self.pillars, self.values, self.convention)
            return interpolator.interpolate(pillar)

    def parallel_bump(self, bump=0.0001):
        self.values = np.array(self.values) + bump
        return

    def pillar_bump(self, pillar, bump=0.0001):
        self.values[self.pillars.index(pillar)] += bump
        return




