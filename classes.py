class Aircraft:
    mission = None
    systems = {}
    f_length = 50
    height = 10.98

    def CG(self):
        total_weight = 0
        numerator = 0
        for name, system in self.systems.items():
            total_weight += system.weight
            numerator += system.weight * system.loc
        return numerator / total_weight

    def z_CG(self):
        total_weight = 0
        numerator = 0
        for name, system in self.systems.items():
            total_weight += system.weight
            numerator += system.weight * (system.z_loc / self.height)
        return numerator / total_weight

    def Ixx(self):
        """
        Calculate Ixx of aircraft with Class II Method (Roskam pg.121)
        divide system.weight by 32.2 to convert lbf to slug
        system.z_loc in ft but self.z_CG() in % aircraft height,
            therefore convert self.z_CG() to ft by multiplying by self.height
        :returns ixx[float] units: slug*ft^2
        """
        ixx = 0
        for name, system in self.systems.items():
            ixx += (system.weight / 32.2) * (system.z_loc - self.z_CG() * self.height) ** 2
        return ixx

    def Iyy(self):
        height = 10.98
        f_length = 50
        iyy = 0
        for name, system in self.systems.items():
            iyy += (system.weight / 32.2) * ((system.loc * f_length - self.CG() * f_length) ** 2 + (
                    system.z_loc - self.z_CG() * height) ** 2)
        return iyy

    def Izz(self):
        height = 10.98
        izz = 0
        for name, system in self.systems.items():
            izz += (system.weight / 32.2) * (system.loc * self.f_length - self.CG() * self.f_length) ** 2
        return izz

    def Izx(self):
        izx = 0
        for name, system in self.systems.items():
            izx += (system.weight / 32.2) * (system.loc * self.f_length - self.CG() * self.f_length) + (
                    system.z_loc - self.z_CG() * self.height)
        return izx

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
    reduction_factor = 0.9

    def __init__(self, name, weight, loc, system_group, z_loc=0):
        self.name = name
        self.weight = weight * self.reduction_factor
        self.loc = loc
        self.z_loc = z_loc
        system_group[self.name] = self
