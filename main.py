from classes import Aircraft, System
import plotting as plot

concept = Aircraft()

wing = System("Wing", 1000, 0.55, concept)
fuel = System("Fuel", 16000, 0.54, concept)
payload = System("Payload", 14000, 0.54, concept)

print(concept.systems)

# plot.CGPlot(concept)
plot.CGExcursion(concept)
