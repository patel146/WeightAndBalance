from astropy import units as u
from astropy.units import imperial as ui
import math

kg_o_m3 = u.kg / u.m ** 3
slug_o_ft3 = ui.slug / ui.ft ** 3
knts = ui.nmi / u.hr


def dyn_pres(dens, speed):
    dens = dens.to(slug_o_ft3)
    speed = speed.to(ui.ft / u.s)
    q = 0.5 * dens * speed ** 2
    return q.to(ui.lbf / ui.ft ** 2)
