from ResolverPop import ResolverPop
from random import random, choice, choices
class ResolverSpecies:
    def __init__(self, gameDict, rowPopulation, colPopulation):
        self.gameDict = gameDict
        self.populations = []
        for i in range(gameDict["resolverPopulations"]):
            self.populations.append(ResolverPop(self.gameDict, rowPopulation, colPopulation))
        self.best = max(list([p.best for p in self.populations]))

    def iterate(self):
        for p in self.populations:
            self.migrate()
            p.iterate()
        self.best = max(list([p.best for p in self.populations]))

    def migrate(self):
        if random() > self.gameDict["resolverMigrationRate"]:
            origin,destination = choices(self.populations, k = 2) 
            exile = choice(origin.population)
            removeForExile = choice(destination.population)
            removeForExile.inheritFrom(exile)

    def guiRow(self, n):
        return self.best.guiRow(n)

    def guiId(self):
        return  self.best.guiId()