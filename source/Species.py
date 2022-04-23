from Pop import Pop
from random import random, choice, choices
class Species:
    def __init__(self, gameDict):
        self.gameDict = gameDict
        self.populations = []
        self.rowPopulations = []
        self.colPopulations = []
        
        for i in range(gameDict["populations"]):
            p = Pop(self.gameDict)
            self.populations.append(p)
            self.rowPopulations.append(p)
        for t in range(gameDict["populationsX"]):
            p = Pop(self.gameDict, gridType = False)
            self.populations.append(p)
            self.colPopulations.append(p)

        self.rowBest = max(list([p.best for p in self.rowPopulations]))
        self.colBest = max(list([p.best for p in self.colPopulations]))



    def iterate(self):
        for p in self.populations:
            self.migrate()
            p.iterate()
            self.rowBest = max(list([p.best for p in self.rowPopulations]))
            self.colBest = max(list([p.best for p in self.colPopulations]))


    def migrate(self):
        if random() > self.gameDict["migrationRate"]:
            origin,destination = choices(self.populations, k = 2)
            
            if origin.gridType == destination.gridType: 
                exile = choice(origin.population)
                removeForExile = choice(destination.population)
                removeForExile.inheritFrom(exile)

    def guiRow(self,n,spacer = "    "):
        return self.rowBest.guiRow(n) + spacer + self.colBest.guiRow(n)

    def guiId(self, spacer = "      "):
        return  self.rowBest.guiId() + spacer + self.colBest.guiId() 