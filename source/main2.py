from parameters import PARAM_DICT as gameDict
from copy import deepcopy
import matplotlib.pyplot as plt
from Pop import Pop as Population
from Species import Species
from ResolverSpecies import ResolverSpecies
from ExperimentRunner import ExperimentRunner

parameters = deepcopy(gameDict)
species = Species(parameters)
pop = [p for p in species.populations if p.gridType]
popX = [p for p in species.populations if not p.gridType]
rSpecies = ResolverSpecies(parameters, pop, popX)
AllSpecies = [species, rSpecies]

runner = ExperimentRunner(AllSpecies, parameters)
runner.run()

for p in species.populations:

    plt.plot(p.history)

plt.show()