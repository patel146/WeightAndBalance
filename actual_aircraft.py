from classes import Aircraft, System
from ClassIIEstimates import estimates, l_f
import plotting as plot
import logger
from CSV_Handler import CAS_SYSTEMS, STEALTH_SYSTEMS, MAX_PAYLOAD_SYSTEMS

system_estimates = {}
wing_pos = 0.51
actual_weights = Aircraft()
actual_weights.mission = "ACTUAL"

actual_weights.systems = system_estimates
actual_weights.mission = "ESTIMATES"

fuel_wing_and_drop_tank = System("Fuel wing + drop tank", 5000*(1/0.9), wing_pos, system_estimates, z_loc=1.06)
fuel_fuselage = System("Fuel fuselage", 4500*(1/0.9), 0.39, system_estimates, z_loc=2.92)

payload_wing = System("Payload wing", 11000*(1/0.9), 0.505, system_estimates, z_loc=0.13)
# payload_internal_bay = System("Payload Internal Bay", 3000, 0.318, system_estimates) ((11.2 / 2) / l_f.value)
gun = System("Gun", 1422*(1/0.9), 0.45, system_estimates, z_loc=0.6)
gun2 = System("Gun", 1422*(1/0.9), 0.45, system_estimates, z_loc=0.6)

pilot = System("Pilot", 250*(1/0.9), 0.17, system_estimates, z_loc=4.23)
# canopy = System("Canopy", 500, 0.1, system_estimates)

# wing = System("Wing", estimates["Wing"], wing_pos, system_estimates)
wing = System("Wing", 2583*(1/0.9), wing_pos, system_estimates,z_loc=1.06)

powerplant = System("Powerplant", 3075*(1/0.9), 0.84, system_estimates, z_loc=3.2)

fuselage = System("Fuselage", 1700*(1/0.9), 0.45, system_estimates, z_loc=3.2)

landing_gear = System("Landing Gear", 1250*(1/0.9), 0.4, system_estimates, z_loc=0.5)

nacelle = System("Nacelle", estimates["Nacelle"], 0.65, system_estimates, z_loc=3.2)

FCS = System("FCS", 850*(1/0.9), 0.38, system_estimates, z_loc=3.2)

VT = System("VT", 361*(1/0.9), 0.88, system_estimates, z_loc=8.1)

HT = System("HT", 235*(1/0.9), 0.92, system_estimates, z_loc=3.2)

APU = System("APU", 110*(1/0.9), 0.3, system_estimates, z_loc=5.6)

avionics = System("Avionics", estimates["Avionics"], 0.214, system_estimates, z_loc=3.27)

fuel_systems = System("Fuel Systems", estimates["Fuel Systems"], 0.6, system_estimates, z_loc=3.2)

elec_systems = System("Elec. Systems", 300*(1/0.9), 0.5, system_estimates, z_loc=3.2)

paint = System("Paint", 85*2*(1/0.9), 0.4, system_estimates, z_loc=3.2)

# man_var = System("Man. Var.", estimates["Manu. Variation"], 0.5, system_estimates, z_loc=3.2)

env_systems = System("Env Systems", estimates["Env. Systems"], 0.3, system_estimates, z_loc=3.2)  # 70.4 lbf

furnishings = System("Furnishings", estimates["Furnishings"], 0.2, system_estimates, z_loc=2.5)

O2_system = System("O2 System", estimates["O2 System"], 0.24, system_estimates, z_loc=3.2)  # 29.5 lbf

armour = System('Pilot Armour', 525*(1/0.9), 0.17, system_estimates, z_loc=4.3)