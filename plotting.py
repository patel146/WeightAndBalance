import matplotlib.pyplot as plt


# Create scatter plot of current aircraft systems
def CGPlot(aircraft):
    x = []
    y = []
    for name, system in aircraft.systems.items():
        x.append(system.loc)
        y.append(system.loc)
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    plt.axvline(x=aircraft.CG(), linestyle='--', color='b', label='CG')
    plt.legend()
    plt.show()


def CGExcursion(aircraft):
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
    plt.xlabel(r"CG [% $l_f$]")
    plt.ylabel(r"$W_T$ [lbf]")
    plt.legend()
    plt.show()
