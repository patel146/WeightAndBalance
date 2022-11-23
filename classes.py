class Aircraft:
    mission = None
    systems = {}

    def CG(self):
        total_weight = 0
        numerator = 0
        for name, system in self.systems.items():
            total_weight += system.weight
            numerator += system.weight * system.loc
        return numerator / total_weight

    def CG_no_HT(self):
        total_weight = 0
        numerator = 0
        for name, system in self.systems.items():
            if name != 'HT':
                total_weight += system.weight
                numerator += system.weight * system.loc
        return numerator / total_weight

    def W_total(self):
        total_weight = 0
        for name, system in self.systems.items():
            total_weight += system.weight
        return total_weight

    def W_e(self):
        total_weight = 0
        for name, system in self.systems.items():
            if name not in ['Fuel wing + drop tank', 'Fuel fuselage', 'Payload wing', 'Gun', 'Payload Internal Bay',
                            'Pilot']:
                total_weight += system.weight
        return total_weight

    def W_no_HT(self):
        total_weight = 0
        for name, system in self.systems.items():
            if name != 'HT':
                total_weight += system.weight
        return total_weight

    def W_f(self):
        return self.systems["Fuel wing + drop tank"].weight + self.systems["Fuel fuselage"].weight

    def FDGW(self):
        return self.W_total() - self.W_f()

    def display_systems(self):
        for name, system in self.systems.items():
            print(name, system.weight, system.loc)


class System:
    def __init__(self, name, weight, loc, system_group):
        self.name = name
        self.weight = weight
        self.loc = loc
        system_group[self.name] = self
