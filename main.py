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

wing_pos = 0.4

concept = Aircraft()

fuel = System("Fuel", 17392, wing_pos, concept)

payload = System("Payload", 7000, wing_pos, concept)
gun = System("Gun", 1084, ((11.2/2)/l_f.value), concept)

wing = System("Wing", estimates["Wing"], wing_pos, concept)

powerplant = System("Powerplant", 4150, 0.85, concept)

fuselage = System("Fuselage", estimates["Fuselage"], 0.45, concept)

landing_gear = System("Landing Gear", estimates["Landing Gear"], 0.45, concept)

nacelle = System("Nacelle", estimates["Nacelle"], 0.5, concept)

FCS = System("FCS", estimates["FCS"], 0.46, concept)

VT = System("VT", estimates["Vertical Tail"], 0.85, concept)
print(estimates["Vertical Tail"])

HT = System("HT", estimates["Horizontal Tail"], 0.95, concept)

APU = System("APU", estimates["APU"], 0.3, concept)

avionics = System("Avionics", estimates["Avionics"], 0.15, concept)

fuel_systems = System("Fuel Systems", estimates["Fuel Systems"], 0.6, concept)

elec_systems = System("Elec. Systems", estimates["Elec. Systems"], 0.5, concept)

paint = System("Paint", estimates["Paint"], 0.4, concept)

man_var = System("Man. Var.", estimates["Manu. Variation"], 0.5, concept)

env_systems = System("Env Systems", estimates["Env. Systems"], 0.3, concept)

furnishings = System("Furnishings", estimates["Furnishings"], 0.2, concept)

O2_system = System("O2 System", estimates["O2 System"], 0.24, concept)

# plot.CGPlot(concept)
# plot.CGExcursion(concept)

logger.log_inputs()
logger.log_results(concept.CG())


    
    
