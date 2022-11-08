'''
Wing Weight

-pg 70 Roskam
Section 5.1.4.1 (For USAF Fighter and Attack AC)
'''

from astropy import units as u
from astropy.units import imperial as ui
import math

estimates = {}


class Estimate:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        estimates[self.name] = self.weight


weights = []
labels = []

kg_o_m3 = u.kg / u.m ** 3
slug_o_ft3 = ui.slug / ui.ft ** 3
knts = ui.nmi / u.hr

# Kw  = 1 for fixed wing and 1.175 for variable sweep
K_w = 1.0

Λ_LE = 35 * u.deg

n_ult = 9

t_o_c = 0.09  # thickness to chord ratio

λ = 0.4  # wing taper ratio

A = 5.5  # aspect ratio (using A instead of AR becuase Roskam uses A)

S = 651.43 * ui.ft ** 2  # wing area

W_TO = 59839 * ui.lbf  # MTOW for critical mission

# convert degrees to radians for easier calculations
Λ_LE = Λ_LE.to(u.rad)


# Wing Weight Function pg.70
def W_w(K_w, Λ_LE, n_ult, t_o_c, λ, A, S, W_TO):
    b1 = K_w * n_ult * W_TO.value * (1 / t_o_c)
    assert Λ_LE.unit == 'rad'
    b2_1 = math.tan(Λ_LE.value)
    b2_2 = (2 * (1 - λ)) / (A * (1 + λ))
    b2 = ((b2_1 - b2_2) ** 2 + 1) * 10 ** -6
    b3 = A * (1 + λ)
    return 3.08 * (b1 * b2) ** 0.593 * b3 ** 0.89 * S.value ** 0.741


W_w = W_w(K_w, Λ_LE, n_ult, t_o_c, λ, A, S, W_TO)
weights.append(W_w)
labels.append('Wing')


'''
Horizontal Tail Weight

- pg.73 Roskam 
(Section 5.2.2.1 GD Method)
Using this method because according to Section 5.2.4 on pg.75, I should, lmao'''

S_h = 157.58 * ui.ft ** 2
b_h = 30 * ui.ft
t_r_h = 0.5 * ui.ft
c_bar = 10.83 * ui.ft
l_h = 19 * ui.ft


def W_h(W_TO, n_ult, S_h, b_h, t_r_h, c_bar, l_h):
    curl_brackets = (W_TO * n_ult) ** 0.813 * S_h ** 0.584 * (b_h / t_r_h) ** 0.033 * (c_bar / l_h) ** 0.28
    return 0.0034 * curl_brackets ** 0.915


W_h = W_h(W_TO, n_ult, S_h, b_h, t_r_h, c_bar, l_h)
weights.append(W_h.value)
labels.append('Horizontal Tail')


'''
Vertical Tail Weight

-pg 73 Roskam
(Section 5.2.2.1 GD Method)'''

z_h = 0  # As long as horizontal stablilizer is not mounted on vertical tail, equation is simplified
M_H = 0.95  # Maximum mach number at sea level
A_v = 5.5  # Aspect ratio of vertical tail
S_v = 100 * ui.ft ** 2  # vertical tail area
l_v = 14 * ui.ft  # vertical tail location
S_r = 20 * ui.ft ** 2  # rudder area
λ_v = 0.1  # vertical tail taper ratio
Λ_qtrchrd_v = 10 * u.deg  # vertical tail quarter chord sweep angle

Λ_qtrchrd_v = Λ_qtrchrd_v.to(u.rad)


def W_v(W_TO, n_ult, S_v, M_H, l_v, S_r, A_v, λ_v, Λ_qtrchrd_v):
    assert Λ_qtrchrd_v.unit == 'rad'
    curly_bracket = (W_TO * n_ult) ** 0.363 * S_v ** 1.089 * M_H ** 0.601 * l_v ** -0.726 * (1 + S_r / S_v) ** 0.217 * \
                    A_v ** 0.337 * (1 + λ_v) ** 0.363 * math.cos(Λ_qtrchrd_v.value) ** -0.484

    return 0.19 * curly_bracket ** 1.014


W_v = W_v(W_TO, n_ult, S_v, M_H, l_v, S_r, A_v, λ_v, Λ_qtrchrd_v)
weights.append(W_v.value)
labels.append('Vertical Tail')


'''
Fuselage Weight

-pg. 76 Roskam
(Section 5.3.2.1 GD Method)
Equation 5.26'''

K_inl = 1.25  # for aircraft with inlets integrated into the fuselage (pg.77)


def dyn_pres(dens, speed):
    dens = dens.to(slug_o_ft3)
    speed = speed.to(ui.ft / u.s)
    q = 0.5 * dens * speed ** 2
    return q.to(ui.lbf / ui.ft ** 2)


q_bar_D = dyn_pres(0.4135 * kg_o_m3, 400 * knts)  # design dive dynamic pressure in psf (pounds per sq.ft)
l_f = 60 * ui.ft  # length of fuselage (should be in ft)
h_f = 15 * ui.ft  # maximum fuselage height (should be in ft)


def W_f(K_inl, q_bar_D, W_TO, l_f, h_f):
    return 10.43 * K_inl ** 1.42 * (q_bar_D / 100) ** 0.283 * (W_TO / 1000) ** 0.95 * (l_f / h_f) ** 0.71


W_f = W_f(K_inl, q_bar_D, W_TO, l_f, h_f)
weights.append(W_f.value)
labels.append('Fuselage')

'''
Engine Nacelle Weight

-pg.80 Roskam
(Section 5.4.2.1) 
Section 5.4.4 said to use eqs. 5.34 or 5.35 for attack aircraft'''

N_inl = 2  # number of inlets
A_inl = 5 * ui.ft ** 2  # capture area per inlet in ft^2
l_n = 10 * ui.ft  # nacelle length from inlet to compressor face
P_2 = 30 * (ui.lbf / ui.inch ** 2)  # max static pressure at engine compressor face in psi (ranges from 15 to 50 psi)


def W_n(N_inl, A_inl, l_n, P_2):
    curly = A_inl ** 0.5 * l_n * P_2
    W_n = 7.435 * N_inl * curly ** 0.731
    return W_n.value


W_n = W_n(N_inl, A_inl, l_n, P_2)
weights.append(W_n)
labels.append('Nacelle')

'''
Landing Gear Weight Estimation

-pg 80 Roskam
(Section 5.5.4 Fighter and Attack Airplanes reccommends using eqs. 5.41 and 5.42)
Will use eq.5.41 for now'''


def W_g(W_TO):
    W_g = 62.21 * (W_TO / 1000) ** 0.84
    return W_g.value


W_g = W_g(W_TO)
weights.append(W_g)
labels.append('Landing Gear')

'''
Power Plant Weight

For now, will just assume value for 2 F404-GE-402 engines (used in F-18)
assuming each engine weighs 2282 lbf'''

W_pwr = 8920
weights.append(W_pwr)
labels.append('Powerplant')

'''
Fuel Systems Weight

-pg.92 Roskam
(Section 6.4.2.1)
assuming self-sealing bladder tanks'''

W_F = 19843 * ui.lbf  # mission fuel weight including reserves
K_fsp = 6.55 * (ui.lbf / ui.gallon)  # just a constant defined in pg. 91, assuming we are using JP-4 jet fuel
W_supp = 7.91 * ((W_F / K_fsp) / 100) ** 0.854


def W_fs(W_F, K_fsp, W_supp):
    curly = (W_F / K_fsp) / 100
    W_fs = 41.6 * curly.value ** 0.818 + W_supp.value
    return W_fs


W_fs = W_fs(W_F, K_fsp, W_supp)
weights.append(W_fs)
labels.append('Fuel Systems')

'''
Flight Control System Weight

-pg.100
(Section 7.1.4.1)
'''

K_fcf = 138  # pg.100


def W_fc(W_TO, K_fcf):
    W_fc = K_fcf * (W_TO / 1000) ** 0.581
    return W_fc.value


W_fc = W_fc(W_TO, K_fcf)

weights.append(W_fc)
labels.append('FCS')

'''
Hydraulic and Pneumatic System Weight

-pg.100
(Included in flight control system weight (W_fc))'''
####################################################################################################################

'''
Instrumentation, Avionics and Electronics System Weight Estimation

-pg.103
(Section 7.4.2.1 USAF Attack Aircraft)
In book, W_i is used but really it refers to W_iae'''

N_pil = 1  # number of pilots
N_e = 2  # number of engines


def W_iae(N_pil, W_TO, N_e):
    W_TO = W_TO.value
    curl1 = 15 + 0.032 * (W_TO / 1000)
    curl2 = 5 + 0.006 * (W_TO / 1000)
    Other_inst = 0.15 * (W_TO / 1000) + 0.012 * W_TO
    W_iae = N_pil * curl1 + N_e * curl2 + Other_inst
    return W_iae


W_iae = W_iae(N_pil, W_TO, N_e)
weights.append(W_iae)
labels.append('Avionics')

'''
Electrical System Weight Estimation

-pg.102
(Section 7.3.4.1 USAF Attack Aircraft)'''


def W_els(W_fs, W_iae):
    curl = (W_fs + W_iae) / 1000
    W_els = 426 * curl ** 0.51
    return W_els


W_els = W_els(W_fs, W_iae)
weights.append(W_els)
labels.append('Elec. Systems')

'''
Air Conditioning, Pressurization, Anti/Deicing Systems Weights (W_api)

-pg.104
(Section 7.5.4.1)'''

N_cr = 1  # number of crew (Should refer to pilots plus anybody else on board)


def W_api(W_iae, N_cr):
    curl = (W_iae + 200 * N_cr) / 1000
    W_api = 202 * curl ** 0.735
    return W_api


W_api = W_api(W_iae, N_cr)
weights.append(W_api)
labels.append('Env. Systems')

'''
Oxygen System Weight

-pg.106
(Section 7.6.4.1'''


def W_ox(N_cr):
    return 16.9 * N_cr ** 1.494


W_ox = W_ox(N_cr)
weights.append(W_ox)
labels.append('O2 System')

'''
Auxiliary Power Unit Weight (APU)

-pg.107
Eq.7.40'''

APU_est_factor = 0.013  # range between 0.004 to 0.013 from the equation

W_apu = APU_est_factor * W_TO

weights.append(W_apu.value)
labels.append('APU')

'''
Furnishings

-pg.109
(Section 7.8.4)
In this case refers to ejection seats and emergency equipment'''


def W_fur(N_cr, q_bar_D, W_TO):
    ejection_seats = 22.9 * ((N_cr * q_bar_D) / 100) ** 0.743
    equip = 107 * ((N_cr * W_TO) / 100000) ** 0.585
    equip = equip.value
    ejection_seats = ejection_seats.value
    return ejection_seats + equip


W_fur = W_fur(N_cr, q_bar_D, W_TO)

weights.append(W_fur)
labels.append('Furnishings')

'''
Payload Weight

-pg.111
just use payload weight for now'''

W_pay = 14000 * ui.lbf

weights.append(W_pay.value)
labels.append('Payload')

'''
Aux Gear (Manufacturers variation)

-pg.111
Eq. 7.50'''

W_E = W_TO - W_pay - W_F


def W_aux(W_E):
    return 0.01 * W_E


W_aux = W_aux(W_E)

weights.append(W_aux.value)
labels.append('Manu. Variation')

'''
Paint Weight

-pg.112
(Eq.7.51)'''

PAINT_EST_FACTOR = 0.006  # ranges from 0.003 to 0.006, beging conservative considering stealth paint might be used


def W_pt(W_TO):
    return PAINT_EST_FACTOR * W_TO


W_pt = W_pt(W_TO)

weights.append(W_pt.value)
labels.append('Paint')

weights.append(W_F.value)
labels.append('Fuel')

for name, weight in zip(labels, weights):
    Estimate(name, weight)

# print("Empty Weight: ", W_E.value)
#
# W_total = sum(weights)
# print('Total Weight: ', W_total)

# print(weights)
# print(labels)

inputs = locals().copy()

# with open("Week8/inputs.txt", "a") as datafile:
#     for d in inputs:
#         datafile.write(d+"\n")

# zipped = list(zip(labels,weights))
# print(zipped)

# with open("data.txt", "a") as datafile:
#     for index, w in enumerate(weights):
#         datafile.write(labels[index]+"\t"+str(w)+"\n")

print(labels)