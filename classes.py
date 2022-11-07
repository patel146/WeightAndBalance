class Aircraft:
    systems = {}

    def CG(self):
        total_weight = 0
        numerator = 0
        for name, system in self.systems.items():
            total_weight += system.weight
            numerator += system.weight * system.loc
        return numerator / total_weight

    def W_total(self):
        total_weight = 0
        for name, system in self.systems.items():
            total_weight += system.weight
        return total_weight


class System:
    def __init__(self, name, weight, loc, aircraft):
        self.name = name
        self.weight = weight
        self.loc = loc
        aircraft.systems[self.name] = self
