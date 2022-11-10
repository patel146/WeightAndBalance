import matplotlib.pyplot as plt

from classes import Aircraft, System
from ClassIIEstimates import estimates, l_f
import plotting as plot
import logger

# TODO recursive fuel and wing location as close to CG as possible ******
# TODO do CG as percentage of MAC
# TODO radar - 250 lbs at nose (around 5% lf)
# TODO radar - 200 lbs between nose and cockpit(around 5% lf)
# TODO find CG wing distance to CG of aircraft
# TODO find lv and lh

# TODO find t_r_h (maximum root thickness)
# TODO find AR of VT
# TODO find rudder area
# TODO find VT taper ratio
# TODO find max fuselage height

wing_pos = 0.4

concept = Aircraft()

fuel = System("Fuel", 17392, wing_pos, concept)

payload = System("Payload", 7000, wing_pos, concept)

pilot = System("Pilot", 250, 0.15, concept)

gun = System("Gun", 1084, ((11.2 / 2) / l_f.value), concept)

wing = System("Wing", estimates["Wing"], wing_pos, concept)

powerplant = System("Powerplant", 4150, 0.85, concept)

fuselage = System("Fuselage", estimates["Fuselage"], 0.45, concept)

landing_gear = System("Landing Gear", estimates["Landing Gear"], 0.45, concept)

nacelle = System("Nacelle", estimates["Nacelle"], 0.5, concept)

FCS = System("FCS", estimates["FCS"], 0.46, concept)

VT = System("VT", estimates["Vertical Tail"], 0.85, concept)

HT = System("HT", estimates["Horizontal Tail"], 0.95, concept)

APU = System("APU", estimates["APU"], 0.3, concept)

avionics = System("Avionics", estimates["Avionics"], 0.15, concept)

fuel_systems = System("Fuel Systems", estimates["Fuel Systems"], 0.6, concept)

elec_systems = System("Elec. Systems", estimates["Elec. Systems"], 0.5, concept)

paint = System("Paint", estimates["Paint"], 0.4, concept)

man_var = System("Man. Var.", estimates["Manu. Variation"], 0.5, concept)

env_systems = System("Env Systems", estimates["Env. Systems"], 0.3, concept) #70.4 lbf

furnishings = System("Furnishings", estimates["Furnishings"], 0.2, concept)

O2_system = System("O2 System", estimates["O2 System"], 0.24, concept) #29.5 lbf


# plot.CGPlot(concept)
# plot.CGExcursion(concept)

# logger.log_inputs()
# logger.log_results(concept.CG())
# logger.log_weights(concept)

def solve_wing_pos():
    diff = concept.CG() - wing.loc
    wing.loc += diff
    fuel.loc += diff
    payload.loc += diff
    diff = concept.CG() - wing.loc
    if diff > 0.001:
        solve_wing_pos()


solve_wing_pos()

results = {"CG": [concept.CG(), '% l_f'],
           "Optimal Wing Pos": [wing.loc, '%_f'],
           "Wing Weight": [wing.weight, 'lbf'],
           "CG VT": [VT.loc, '% l_f'],
           "CG HT": [HT.loc, '% l_f'],
           "CG w/out HT": [concept.CG_no_HT(), '% l_f']}

logger.create_log_file(results, concept)
