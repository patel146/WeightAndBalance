import matplotlib.pyplot as plt
import tkinter as tk

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

# TODO get ac empty weight

wing_pos = 0.51


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

system_estimates = {}
concept_weight_estimates = Aircraft()

concept_weight_estimates.systems = system_estimates
concept_weight_estimates.mission = "ESTIMATES"

fuel_wing_and_drop_tank = System("Fuel wing + drop tank", 5000*(1/0.9), wing_pos, system_estimates, z_loc=1.06)
fuel_fuselage = System("Fuel fuselage", 4500*(1/0.9), 0.39, system_estimates, z_loc=2.92)

payload_wing = System("Payload wing", 11000*(1/0.9), 0.505, system_estimates, z_loc=0.13)
# payload_internal_bay = System("Payload Internal Bay", 3000, 0.318, system_estimates) ((11.2 / 2) / l_f.value)
gun = System("Gun", 1040*(1/0.9), 0.45, system_estimates, z_loc=0.6)
gun2 = System("Gun", 1040*(1/0.9), 0.45, system_estimates, z_loc=0.6)

pilot = System("Pilot", 250*(1/0.9), 0.17, system_estimates, z_loc=4.23)
# canopy = System("Canopy", 500, 0.1, system_estimates)

# wing = System("Wing", estimates["Wing"], wing_pos, system_estimates)
wing = System("Wing", 2732*(1/0.9), wing_pos, system_estimates,z_loc=1.06)

powerplant = System("Powerplant", 3034*(1/0.9), 0.84, system_estimates, z_loc=3.2)

fuselage = System("Fuselage", estimates['Fuselage'], 0.45, system_estimates, z_loc=3.2)

landing_gear = System("Landing Gear", 1200, 0.4, system_estimates, z_loc=0.5)

nacelle = System("Nacelle", estimates["Nacelle"], 0.65, system_estimates, z_loc=3.2)

FCS = System("FCS", 850*(1/0.9), 0.38, system_estimates, z_loc=3.2)

VT = System("VT", estimates["Vertical Tail"], 0.88, system_estimates, z_loc=8.1)

HT = System("HT", estimates["Horizontal Tail"], 0.92, system_estimates, z_loc=3.2)

APU = System("APU", estimates["APU"], 0.3, system_estimates, z_loc=5.6)

avionics = System("Avionics", estimates["Avionics"], 0.214, system_estimates, z_loc=3.27)

fuel_systems = System("Fuel Systems", estimates["Fuel Systems"], 0.6, system_estimates, z_loc=3.2)

elec_systems = System("Elec. Systems", estimates["Elec. Systems"], 0.5, system_estimates, z_loc=3.2)

paint = System("Paint", estimates["Paint"], 0.4, system_estimates, z_loc=3.2)

# man_var = System("Man. Var.", estimates["Manu. Variation"], 0.5, system_estimates, z_loc=3.2)

env_systems = System("Env Systems", estimates["Env. Systems"], 0.3, system_estimates, z_loc=3.2)  # 70.4 lbf

furnishings = System("Furnishings", estimates["Furnishings"], 0.2, system_estimates, z_loc=2.5)

O2_system = System("O2 System", estimates["O2 System"], 0.24, system_estimates, z_loc=3.2)  # 29.5 lbf

armour = System('Pilot Armour', 850, 0.17, system_estimates, z_loc=4.3)


def all_missons():
    for concept in aircraft_missions:
        # plot.CGPlot(concept)
        # plot.CGExcursion(concept)
        results = {"CG": [concept.CG(), '% l_f'],
                   "Optimal Wing Pos": [concept.systems['Wing'].loc, '%_f'],
                   "Wing Weight": [concept.systems['Wing'].weight, 'lbf'],
                   "CG VT": [concept.systems['VT'].loc, '% l_f'],
                   "CG HT": [concept.systems['HT'].loc, '% l_f'],
                   "CG w/out HT": [concept.CG_no_HT(), '% l_f'],
                   "Weight w/out HT": [concept.W_no_HT(), 'lbf'],
                   "FDGW": [concept.FDGW(), 'lbf'],
                   "W_T": [concept.W_total(), 'lbf']}

        logger.create_log_file(results, concept)


def calculate_estimates():
    plot.CGPlot(concept_weight_estimates)
    # plot.CGExcursion(concept_weight_estimates)
    results = {"CG": [concept_weight_estimates.CG(), '% l_f'],
               "Optimal Wing Pos": [concept_weight_estimates.systems['Wing'].loc, '%_f'],
               "Wing Weight": [concept_weight_estimates.systems['Wing'].weight, 'lbf'],
               "Empty Weight": [concept_weight_estimates.W_e(), 'lbf'],
               "CG VT": [concept_weight_estimates.systems['VT'].loc, '% l_f'],
               "CG HT": [concept_weight_estimates.systems['HT'].loc, '% l_f'],
               "CG w/out HT": [concept_weight_estimates.CG_no_HT(), '% l_f'],
               "Weight w/out HT": [concept_weight_estimates.W_no_HT(), 'lbf'],
               "FDGW": [concept_weight_estimates.FDGW(), 'lbf'],
               "W_T": [concept_weight_estimates.W_total(), 'lbf']
               }
    logger.create_log_file(results, concept_weight_estimates)


# logger.log_inputs()
# logger.log_results(concept.CG())
# logger.log_weights(concept)

def solve_wing_pos(aircraft):
    # print(aircraft.systems['Wing'].loc)
    diff = aircraft.CG() - aircraft.systems['Wing'].loc
    aircraft.systems['Wing'].loc += diff
    aircraft.systems['Payload wing'].loc += diff
    aircraft.systems['Fuel wing + drop tank'].loc += diff
    diff = aircraft.CG() - aircraft.systems['Wing'].loc
    if diff > 0.001:
        solve_wing_pos(aircraft)


# plot.MTOW_Track()
# plot.CGPlot(concept_weight_estimates)

# concept_weight_estimates.display_systems()
# plot.CG_EXC_2(concept_weight_estimates)
#
# # solve_wing_pos(concept)
calculate_estimates()

print(concept_weight_estimates.W_total())

# window = tk.Tk()
# label = tk.Label(window, text='Test')
# label.place(x=0, y=0)
#
# button = tk.Button(window, text='calculate', command=calculate_estimates)
# button.grid(row=0, column=1)
#
# in1 = tk.Entry(window)
# in1.grid(row=1, column=1)
#
# window.mainloop()
