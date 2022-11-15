import matplotlib.pyplot as plt

from classes import Aircraft, System
from ClassIIEstimates import estimates, l_f
import plotting as plot
import logger
from CSV_Handler import CAS_SYSTEMS, STEALTH_SYSTEMS, MAX_PAYLOAD_SYSTEMS

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

wing_pos = 0.49

concept_max_payload = Aircraft()

concept_max_payload.systems = MAX_PAYLOAD_SYSTEMS
concept_max_payload.mission = "MAX PAYLOAD"

concept_CAS = Aircraft()

concept_CAS.systems = CAS_SYSTEMS
concept_CAS.mission = "CAS"

concept_stealth = Aircraft()

concept_stealth.systems = STEALTH_SYSTEMS
concept_stealth.mission = "STEALTH"

aircraft_missions = [concept_stealth, concept_CAS, concept_max_payload]

# fuel_wing_and_drop_tank = System("fuel_wing_and_drop_tank", 9000, 0.49, concept)
# fuel_fuselage = System("fuel_fuselage", 6400, 0.52, concept)
#
# payload_wing = System("Payload Wing", 1600, 0.49, concept)
# payload_internal_bay = System("Payload Internal Bay", 3000, 0.318, concept)
# gun = System("Gun", 1084, ((11.2 / 2) / l_f.value), concept)
#
# pilot = System("Pilot", 250, 0.15, concept)
# canopy = System("Canopy", 500, 0.1, concept)
#
# wing = System("Wing", 3451, wing_pos, concept)
#
# powerplant = System("Powerplant", 3200, 0.85, concept)
#
# fuselage = System("Fuselage", estimates["Fuselage"], 0.45, concept)
#
# landing_gear = System("Landing Gear", estimates["Landing Gear"], 0.4, concept)
#
# nacelle = System("Nacelle", estimates["Nacelle"], 0.5, concept)
#
# FCS = System("FCS", estimates["FCS"], 0.38, concept)
#
# VT = System("VT", estimates["Vertical Tail"], 0.85, concept)
#
# HT = System("HT", estimates["Horizontal Tail"], 0.975, concept)
#
# APU = System("APU", estimates["APU"], 0.3, concept)
#
# avionics = System("Avionics", estimates["Avionics"], 0.15, concept)
#
# fuel_systems = System("Fuel Systems", estimates["Fuel Systems"], 0.6, concept)
#
# elec_systems = System("Elec. Systems", estimates["Elec. Systems"], 0.5, concept)
#
# paint = System("Paint", estimates["Paint"], 0.4, concept)
#
# man_var = System("Man. Var.", estimates["Manu. Variation"], 0.5, concept)
#
# env_systems = System("Env Systems", estimates["Env. Systems"], 0.3, concept)  # 70.4 lbf
#
# furnishings = System("Furnishings", estimates["Furnishings"], 0.2, concept)
#
# O2_system = System("O2 System", estimates["O2 System"], 0.24, concept)  # 29.5 lbf

# armour = System('Pilot Armour', 1000, 0.15, concept)

for concept in aircraft_missions:
    plot.CGPlot(concept)
    plot.CGExcursion(concept)
    results = {"CG": [concept.CG(), '% l_f'],
               "Optimal Wing Pos": [concept.systems['Wing'].loc, '%_f'],
               "Wing Weight": [concept.systems['Wing'].weight, 'lbf'],
               "CG VT": [concept.systems['VT'].loc, '% l_f'],
               "CG HT": [concept.systems['HT'].loc, '% l_f'],
               "CG w/out HT": [concept.CG_no_HT(), '% l_f']}

    # logger.create_log_file(results, concept)


# logger.log_inputs()
# logger.log_results(concept.CG())
# logger.log_weights(concept)

def solve_wing_pos(aircraft):
    # print(aircraft.systems['Wing'].loc)
    diff = concept.CG() - aircraft.systems['Wing'].loc
    aircraft.systems['Wing'].loc += diff
    aircraft.systems['Payload wing'].loc += diff
    aircraft.systems['Fuel wing + drop tank'].loc += diff
    diff = concept.CG() - aircraft.systems['Wing'].loc
    if diff > 0.001:
        solve_wing_pos(aircraft)


# solve_wing_pos(concept)


