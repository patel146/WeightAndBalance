import pandas as pd
from astropy import units as u
from astropy.units import imperial as ui
from classes import System

inputs = pd.read_csv("INPUTS.csv")
inputs = inputs.set_index("Variable")

units = {'u.deg': u.deg,
         '-': 1,
         'ui.ft ** 2': ui.ft ** 2,
         'ui.lbf': ui.lbf,
         'ui.ft': ui.ft,
         '(ui.lbf / ui.inch ** 2)': (ui.lbf / ui.inch ** 2),
         '(ui.lbf / ui.gallon)': (ui.lbf / ui.gallon),
         }

K_w = inputs.loc["K_w"].values[0]
Λ_LE = inputs.loc["Λ_LE"].values[0] * units[inputs.loc["Λ_LE"].values[1]]
n_ult = inputs.loc["n_ult"].values[0] * units[inputs.loc["n_ult"].values[1]]
t_o_c = inputs.loc["t_o_c"].values[0] * units[inputs.loc["t_o_c"].values[1]]
λ = inputs.loc["λ"].values[0] * units[inputs.loc["λ"].values[1]]
A = inputs.loc["A"].values[0] * units[inputs.loc["A"].values[1]]
S = inputs.loc["S"].values[0] * units[inputs.loc["S"].values[1]]
W_TO = inputs.loc["W_TO"].values[0] * units[inputs.loc["W_TO"].values[1]]
S_h = inputs.loc["S_h"].values[0] * units[inputs.loc["S_h"].values[1]]
b_h = inputs.loc["b_h"].values[0] * units[inputs.loc["b_h"].values[1]]
t_r_h = inputs.loc["t_r_h"].values[0] * units[inputs.loc["t_r_h"].values[1]]
c_bar = inputs.loc["c_bar"].values[0] * units[inputs.loc["c_bar"].values[1]]
l_h = inputs.loc["l_h"].values[0] * units[inputs.loc["l_h"].values[1]]
z_h = inputs.loc["z_h"].values[0] * units[inputs.loc["z_h"].values[1]]
M_H = inputs.loc["M_H"].values[0] * units[inputs.loc["M_H"].values[1]]
A_v = inputs.loc["A_v"].values[0] * units[inputs.loc["A_v"].values[1]]
S_v = inputs.loc["S_v"].values[0] * units[inputs.loc["S_v"].values[1]]
l_v = inputs.loc["l_v"].values[0] * units[inputs.loc["l_v"].values[1]]
S_r = inputs.loc["S_r"].values[0] * units[inputs.loc["S_r"].values[1]]
λ_v = inputs.loc["λ_v"].values[0] * units[inputs.loc["λ_v"].values[1]]
Λ_qtrchrd_v = inputs.loc["Λ_qtrchrd_v"].values[0] * units[inputs.loc["Λ_qtrchrd_v"].values[1]]
K_inl = inputs.loc["K_inl"].values[0] * units[inputs.loc["K_inl"].values[1]]
l_f = inputs.loc["l_f"].values[0] * units[inputs.loc["l_f"].values[1]]
h_f = inputs.loc["h_f"].values[0] * units[inputs.loc["h_f"].values[1]]
N_inl = inputs.loc["N_inl"].values[0] * units[inputs.loc["N_inl"].values[1]]
A_inl = inputs.loc["A_inl"].values[0] * units[inputs.loc["A_inl"].values[1]]
l_n = inputs.loc["l_n"].values[0] * units[inputs.loc["l_n"].values[1]]
P_2 = inputs.loc["P_2"].values[0] * units[inputs.loc["P_2"].values[1]]
W_pwr = inputs.loc["W_pwr"].values[0] * units[inputs.loc["W_pwr"].values[1]]
W_F = inputs.loc["W_F"].values[0] * units[inputs.loc["W_F"].values[1]]
K_fsp = inputs.loc["K_fsp"].values[0] * units[inputs.loc["K_fsp"].values[1]]
N_pil = inputs.loc["N_pil"].values[0] * units[inputs.loc["N_pil"].values[1]]
N_e = inputs.loc["N_e"].values[0] * units[inputs.loc["N_e"].values[1]]
K_fcf = inputs.loc["K_fcf"].values[0] * units[inputs.loc["K_fcf"].values[1]]
APU_est_factor = inputs.loc["APU_est_factor"].values[0] * units[inputs.loc["APU_est_factor"].values[1]]
W_pay = inputs.loc["W_pay"].values[0] * units[inputs.loc["W_pay"].values[1]]
PAINT_EST_FACTOR = inputs.loc["PAINT_EST_FACTOR"].values[0] * units[inputs.loc["PAINT_EST_FACTOR"].values[1]]

all_missions = pd.read_csv("MISSIONS.csv")
CAS_data = all_missions.loc[:, ['SYSTEM', 'CAS', 'CAS loc']]
CAS_data.columns = CAS_data.iloc[0]
CAS_data = CAS_data.drop(CAS_data.index[0])
CAS_data = CAS_data.set_index('system')

CAS_SYSTEMS = {}
for data in CAS_data.iterrows():
    name = data[0]
    info = data[1]
    weight = info[0]
    loc = info[1]
    # print(f"{name} weighs {weight} at {loc}")
    System(name, float(weight), float(loc), CAS_SYSTEMS)


