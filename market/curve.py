

class Curve:

    def __init__(self, pillars, values):
        self.pillars = pillars
        self.values = values

    def get_value(self, pillar):
        return self.values[self.pillars.index(pillar)]




