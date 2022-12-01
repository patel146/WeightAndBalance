import matplotlib.pyplot as plt

font = {'family': 'sans-serif',
        # 'weight' : 'bold',
        'size': 12}

plt.rc('font', **font)


# Create scatter plot of current aircraft systems
def CGPlot(aircraft):
    fig, ax = plt.subplots()
    x = []
    y = []
    labels = []
    for name, system in aircraft.systems.items():
        x.append(system.loc)
        y.append(system.weight)
        ax.annotate(name, xy=(system.loc, system.weight), xycoords='data',
                    xytext=(system.loc, system.weight), textcoords='data',
                    horizontalalignment='right', verticalalignment='top',
                    )

    print("CG: ", aircraft.CG())
    ax.scatter(x, y)
    plt.axvline(x=aircraft.CG(), linestyle='--', color='b', label='CG')
    plt.xlabel('CG location [$\% l_f$]')
    plt.ylabel('Weight [lb$_f$]')
    plt.legend()
    plt.title(aircraft.mission)
    plt.show()


def CG_MAC(l_f, wing_pos, CG):
    MAC = 10.45 / l_f
    LEMAC = wing_pos - (MAC / 22)
    TEMAC = wing_pos + (MAC / 2)
    return (CG - LEMAC) / MAC


def interpolate(x1, x2):
    return (x1 + x2) / 2


def CGExcursion(aircraft):
    l_f = 49.5
    wing_pos = 0.49
    initial_CG = CG_MAC(l_f, wing_pos, aircraft.CG())
    static_margin = 0.0625
    fig, ax = plt.subplots()
    x = []
    y = []

    def burn(name):
        while aircraft.systems[name].weight > 1:
            aircraft.systems[name].weight -= 1
            x.append(CG_MAC(l_f, wing_pos, aircraft.CG()))
            y.append(aircraft.W_total())

        ax.plot(x, y, color='k')
        ys = len(y)
        off_x = 0.01
        ax.annotate(name, xy=(x[-int(ys / 2)], y[-int(ys / 2)]), xycoords='data',
                    xytext=(x[-int(ys / 2)] + off_x, y[-int(ys / 2)]), textcoords='data',
                    arrowprops=dict(facecolor='black', shrink=0.005, headwidth=2, width=0.1, headlength=4),
                    horizontalalignment='left', verticalalignment='top', )
        del x[:-1]
        del y[:-1]

    def drop(name):
        aircraft.systems[name].weight = 0
        x.append(CG_MAC(l_f, wing_pos, aircraft.CG()))
        y.append(aircraft.W_total())
        ax.plot(x, y, color="k", label=name)
        ys = len(y)
        off_x = -0.04
        up_y = 1000
        ax.annotate(name, xy=(x[-int(ys / 2)], y[-int(ys / 2)] + up_y), xycoords='data',
                    xytext=(x[-int(ys / 2)] + off_x, y[-int(ys / 2)] + up_y), textcoords='data',
                    arrowprops=dict(facecolor='black', shrink=0.005, headwidth=2, width=0.1, headlength=4),
                    horizontalalignment='left', verticalalignment='top', )
        del x[:-1]
        del y[:-1]

    def shoot_cannons(ammo_weight):
        aircraft.systems["Gun"].weight -= ammo_weight
        x.append(CG_MAC(l_f, wing_pos, aircraft.CG()))
        y.append(aircraft.W_total())
        ax.plot(x, y, color="k", label="Shoot Cannons")
        ys = len(y)
        off_x = 0.01
        up_y = 1000
        arrow_x = interpolate(x[0], x[-1])
        arrow_y = interpolate(y[0], y[-1])
        ax.annotate("Shoot Ammo", xy=(arrow_x, arrow_y), xycoords='data',
                    xytext=(arrow_x + off_x, arrow_y + up_y), textcoords='data',
                    arrowprops=dict(facecolor='black', shrink=0.005, headwidth=2, width=0.1, headlength=4),
                    horizontalalignment='left', verticalalignment='top', )
        del x[:-1]
        del y[:-1]

    if aircraft.systems["Fuel fuselage"].weight != 0:
        burn("Fuel fuselage")
    burn("Fuel wing + drop tank")

    if aircraft.systems["Payload wing"].weight != 0:
        drop("Payload wing")
    shoot_cannons(700)

    # Static Margin
    ax.axvline(x=initial_CG + static_margin, linestyle='--', color='b', label='Static Margin')

    # In flight forward limit
    ax.axvline(x=initial_CG, linestyle='--', color='b', label='Static Margin')

    # Forward CG limit
    ax.axvline(x=CG_MAC(l_f, wing_pos, 0.475), linestyle='--', color='k', label='Forward Limit')

    # Aft CG limit
    ax.axvline(x=CG_MAC(l_f, wing_pos, 0.52), linestyle='--', color='k', label='Aft Limit')

    plt.xlabel(r"CG [% MAC]")
    plt.ylabel(r"$W_T$ [lbf]")
    # plt.legend()
    plt.title(aircraft.mission)
    plt.tight_layout()
    plt.show()


# CG Excursion 2, full mission laid out
# This function specifically made with CAS 3 mission in mind using data from performance
# https://onedrive.live.com/edit.aspx?resid=951C12727E23B89A!843&cid=951c12727e23b89a&CT=1669160633240&OR=ItemsView

def CG_EXC_2(aircraft):
    static_margin = 0.0805
    l_f = 49
    wing_pos = 0.49

    fig, ax = plt.subplots()
    xs = []
    ys = []

    # helper function to quickly plot and annotate points
    def point(CG, W, xoff, yoff, name):
        xs.append(CG_MAC(l_f, wing_pos, CG))
        ys.append(W)
        plt.scatter(CG_MAC(l_f, wing_pos, CG), W, color='k')
        plt.annotate(name, xy=(CG_MAC(l_f, wing_pos, CG), W), xycoords='data',
                     xytext=(CG_MAC(l_f, wing_pos, CG) + xoff, W + yoff), textcoords='data',
                     arrowprops=dict(arrowstyle="->",
                                     connectionstyle="arc3")
                     )

    # helper function to get point given fuel fraction and fuel tank to be used (only for cruise, climb) NOT payload
    def after(name, fuel_tank, fuel_fraction, plot=False):
        ff = fuel_fraction
        if fuel_tank == 'Fuel fuselage':
            aircraft.systems[fuel_tank].weight = fuel_fraction * aircraft.systems[fuel_tank].weight + (ff - 1) * \
                                                 aircraft.systems['Fuel wing + drop tank'].weight
        elif fuel_tank == 'Fuel wing + drop tank':
            aircraft.systems[fuel_tank].weight = fuel_fraction * aircraft.systems[fuel_tank].weight + (ff - 1) * \
                                                 aircraft.systems['Fuel fuselage'].weight
        if plot:
            point(aircraft.CG(), aircraft.W_total(), 0, 100, 'After ' + name)

    # plot the starting point (MTOW and whatever the CG is at that point)
    point(aircraft.CG(), aircraft.W_total(), 0, 100, 'Takeoff')

    print(aircraft.W_total())

    before_attack_tank = 'Fuel fuselage'
    # plot aircraft after climb and cruising
    after("climb and cruise", before_attack_tank, 0.994 * 0.944)

    # plot aircraft after loiter
    after("loiter", before_attack_tank, 0.944)

    # plot aircraft after descent
    after("descent", before_attack_tank, 0.999, plot=True)

    print(aircraft.W_total())

    # plot aircraft after attack, assume aircraft drops all payload
    attack_ff = 0.995 * 0.998 * 0.996

    # fuel burned during attack
    aircraft.systems['Fuel fuselage'].weight *= attack_ff
    # all payload dropped during attack
    aircraft.systems['Payload wing'].weight = 0

    aircraft.systems['Gun'].weight -= 1650
    aircraft.systems['Gun2'].weight -= 1650

    point(aircraft.CG(), aircraft.W_total(), 0, 100, "After attack")

    # after climb following attack
    after('climb 2', 'Fuel fuselage', 0.995)

    # after cruise 2
    after('cruise 2', 'Fuel fuselage', 0.941)

    # after descent 2
    after('descent 2', 'Fuel fuselage', 0.999)

    # after reserve
    after('reserve ', 'Fuel fuselage', 0.983)

    # after descent
    after('final descent ', 'Fuel fuselage', 0.999)

    # after landing
    after('landing ', 'Fuel fuselage', 0.995, plot=True)

    # after taxi
    after('taxi ', 'Fuel fuselage', 0.995)

    # deplane (pilot leaves)
    aircraft.systems['Pilot'].weight = 0
    point(aircraft.CG(), aircraft.W_total(), 0, 100, "Deplane")

    # rearm
    aircraft.systems['Payload wing'].weight = 11584.5
    aircraft.systems['Gun'].weight = 1900
    aircraft.systems['Gun2'].weight = 1900
    
    
    point(aircraft.CG(), aircraft.W_total(), 0, 100, "Re-arm")

    # refuel
    aircraft.systems['Fuel fuselage'].weight = 4500
    aircraft.systems['Fuel wing + drop tank'].weight = 5000
    point(aircraft.CG(), aircraft.W_total(), 0, 100, "Refuel")

    # pilot boards
    aircraft.systems['Pilot'].weight = 250
    point(aircraft.CG(), aircraft.W_total(), 0, 100, "")

    plt.plot(xs, ys)

    # CG Limits
    # Static Margin

    ax.axvline(x=CG_MAC(l_f, wing_pos, aircraft.CG()) + static_margin, linestyle='-.', color='b', label='Static Margin')
    # In flight forward limit
    ax.axvline(x=CG_MAC(l_f, wing_pos, 0.44), linestyle='--', color='b', label='In flight forward limit')
    # Forward CG limit
    ax.axvline(x=CG_MAC(l_f, wing_pos, 0.49), linestyle='--', color='k', label='Ground Forward Limit')
    # # Aft CG limit
    ax.axvline(x=CG_MAC(l_f, wing_pos, 0.55), linestyle='-.', color='k', label='Ground Aft Limit')
    # show the plot
    plt.xlabel('CG [% MAC]')
    plt.ylabel('W$_{TOTAL}$ [lb$_f$]')
    plt.legend()
    plt.tight_layout()
    plt.show()


# MTOW tracking plot
def MTOW_Track():
    names = [str(i) for i in range(1, 8)]
    MTOWS = [54291, 40870, 41722, 35608, 35608, 37500, 34790]
    fig, ax = plt.subplots()
    plt.bar(names, MTOWS)
    plt.xlabel('Iteration')
    plt.ylabel('MTOW [lb$_f$]')
    plt.tight_layout()
    plt.show()
