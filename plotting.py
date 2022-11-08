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


def CGExcursion(aircraft):
    initial_CG = aircraft.CG()
    static_margin = 0.08
    fig, ax = plt.subplots()
    x = []
    y = []
    fuel = range(aircraft.systems["Fuel"].weight)
    # Fuel burn
    for i in fuel:
        aircraft.systems["Fuel"].weight -= 1
        x.append(aircraft.CG())
        y.append(aircraft.W_total())

    ax.plot(x, y, label="Fuel Burn")

    del x[:-1]
    del y[:-1]
    # Payload Drop
    aircraft.systems["Payload"].weight = 0
    x.append(aircraft.CG())
    y.append(aircraft.W_total())

    ax.plot(x, y, color="r", label="Payload Drop")

    # Static Margin
    ax.axvline(x=initial_CG+static_margin, linestyle = '--', color='b', label='Static Margin')
    ax.axvspan(0, initial_CG + static_margin, alpha=0.2, label="Stable Region")

    plt.xlabel(r"CG [% $l_f$]")
    plt.xlim([initial_CG * 0.99, initial_CG+static_margin*1.01])
    plt.ylabel(r"$W_T$ [lbf]")
    plt.legend()
    plt.tight_layout()
    plt.show()
