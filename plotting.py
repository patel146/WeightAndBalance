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
    l_f = 54
    wing_pos = 0.52
    initial_CG = CG_MAC(l_f, wing_pos, aircraft.CG())
    static_margin = 0.08
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
                    xytext=(arrow_x+off_x, arrow_y+up_y), textcoords='data',
                    arrowprops=dict(facecolor='black', shrink=0.005, headwidth=2, width=0.1, headlength=4),
                    horizontalalignment='left', verticalalignment='top', )
        del x[:-1]
        del y[:-1]

    burn("Fuel wing + drop tank")
    if aircraft.systems["Fuel fuselage"].weight != 0:
        burn("Fuel fuselage")
    if aircraft.systems["Payload wing"].weight != 0:
        drop("Payload wing")
    shoot_cannons(500)

    # Static Margin
    ax.axvline(x=initial_CG + static_margin, linestyle='--', color='b', label='Static Margin')
    ax.axvspan(0, initial_CG + static_margin, alpha=0.2, label="Stable Region")

    plt.xlabel(r"CG [% MAC]")
    plt.xlim([initial_CG * 0.8, initial_CG + static_margin * 1.4])
    plt.ylabel(r"$W_T$ [lbf]")
    # plt.legend()
    plt.title(aircraft.mission)
    plt.tight_layout()
    plt.show()
