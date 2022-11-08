from classes import Aircraft, System
from ClassIIEstimates import estimates
import plotting as plot

concept = Aircraft()

fuel = System("Fuel", 16000, 0.54, concept)

payload = System("Payload", 14000, 0.54, concept)

wing = System("Wing", estimates["Wing"], 0.55, concept)

powerplant = System("Powerplant", 3750, 0.85, concept)

fuselage = System("Fuselage", estimates["Fuselage"], 0.45, concept)

landing_gear = System("Landing Gear", estimates["Landing Gear"], 0.45, concept)

nacelle = System("Nacelle", estimates["Nacelle"], 0.5, concept)

FCS = System("FCS", estimates["FCS"], 0.2, concept)

VT = System("VT", estimates["Vertical Tail"], 0.85, concept)

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

plot.CGPlot(concept)
plot.CGExcursion(concept)
