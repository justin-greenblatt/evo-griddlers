from copy import deepcopy
from random import shuffle, choices, choice
from math import log
from time import time
from Pop import Pop
from Resolver import Resolver

class ResolverPop(Pop):
    
    def __init__(self,  gameDict, rowHostPopulations, colHostPopulations):
    
        self.population = []

        self.colHostPopulations = colHostPopulations

        self.rowHostPopulations = rowHostPopulations

        self.id = "P#" + str(time())[-3:]
        
        self.gameDict = deepcopy(gameDict)

        self.history = []
        
        self.generations = 0

        self.meanHistory = []
        
        self.best = None

        self.griddler = self.gameDict["griddler"]
        
        self.evalRules = {"rows" : self.gameDict["rowRules"],
                          "cols" : self.gameDict["colRules"]}

        for r in range(self.gameDict["resolverPopulationSize"]):

            self.population.append(Resolver(self))

    def copy(self):
        p = Pop(self, self.rowHostPopulations, self.colHostPopulations, self.gameDict)
        for a,b in zip(p.population, self.population):
            a.inheritFrom(b)
        p.generations = self.generations
        return p

    def reproduceByFitness(self):
        newGen = []
        #important to note that the fitness function is different
        fitnessList = list([1 / i.score for i in self.population])
        Totalfitness = sum(fitnessList)
        normalizedFitness = [f / Totalfitness for f in fitnessList]
        
        for i in range(self.gameDict["resolverPopulationSize"]):

            a,b = choices(self.population,
              weights = normalizedFitness,
              k = 2)
            newGen.append(a.breed(b))

        self.population = newGen

    def crossover(self):
        shuffle(self.population)
        all([a.crossover(b) for a,b in 
            zip(self.population[:round(len(self.population)/2)],
                self.population[round(len(self.population)/2):])])

    def changeHost(self):
        for i in self.population:
            i.changeHost()

    def iterate(self):
    
        self.popEvaluate()
        self.best = self.mostFit()
        self.history.append(self.best.score)
        self.reproduceByFitness()
        self.mutate()
        self.changeHost()
        self.meanHistory.append(self.popMean())
        self.generations +=1