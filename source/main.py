from parameters import PARAM_DICT as gameDict
from random import randint, random
from copy import deepcopy
import matplotlib.pyplot as plt
from Pop import Pop as Population
from Species import Species
from os import system

parameters = deepcopy(gameDict)

species = Species(parameters)

pop = [p for p in species.populations if p.gridType]
popX = [p for p in species.populations if not p.gridType]

rSpecies = ResolverSpecies(parameters, pop, popX)

for i in range(parameters["generations"]):
    
    species.iterate()
    system("clear")
    best = max(list([p.best for p in pop]))
    bestX = max(list([p.best for p in popX]))
    print("Row Optimization: Score {} | Generation {} | PopNumber {}".format(best.score,i,best.population.id))
    best.printMe()

    print("Column Optimization: Score {} | Generation {} | PopNumber {}".format(bestX.score,i,bestX.population.id))
    bestX.printMe()

for p in species.populations:

    plt.plot(p.history)

plt.show()