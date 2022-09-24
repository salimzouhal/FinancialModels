from tools.interpolator import Interpolator

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




