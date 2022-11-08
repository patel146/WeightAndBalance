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
    plt.show()


def CG_MAC(l_f, wing_pos, CG):
    MAC = 10.45 / l_f
    LEMAC = wing_pos - (MAC / 22)
    TEMAC = wing_pos + (MAC / 2)
    return (CG - LEMAC) / MAC


def CGExcursion(aircraft):
    l_f = 54
    wing_pos = 0.546
    initial_CG = CG_MAC(l_f, wing_pos, aircraft.CG())
    static_margin = 0.08
    fig, ax = plt.subplots()
    x = []
    y = []
    fuel = range(aircraft.systems["Fuel"].weight)
    # Fuel burn
    for i in fuel:
        aircraft.systems["Fuel"].weight -= 1
        x.append(CG_MAC(l_f, wing_pos, aircraft.CG()))
        y.append(aircraft.W_total())

    ax.plot(x, y, label="Fuel Burn")

    del x[:-1]
    del y[:-1]
    # Payload Drop
    aircraft.systems["Payload"].weight = 0
    x.append(CG_MAC(l_f, wing_pos, aircraft.CG()))
    y.append(aircraft.W_total())

    ax.plot(x, y, color="r", label="Payload Drop")

    # Static Margin
    ax.axvline(x=initial_CG + static_margin, linestyle='--', color='b', label='Static Margin')
    ax.axvspan(0, initial_CG + static_margin, alpha=0.2, label="Stable Region")

    plt.xlabel(r"CG [% MAC]")
    plt.xlim([initial_CG * 0.8, initial_CG + static_margin * 1.4])
    plt.ylabel(r"$W_T$ [lbf]")
    plt.legend()
    plt.tight_layout()
    plt.show()
