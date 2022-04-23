from SlideGridX import SlideGridX
from itertools import cycle
from copy import deepcopy
from SlideGrid import SlideGrid
import regex
from random import shuffle,choices
from math import log
from time import time
class Pop:
    
    def __init__(self,gameDict, gridType = True):
    
        self.population = []

        self.id = "P#" + str(time())[-3:]
        
        self.gameDict = deepcopy(gameDict)
        
        self.gridType = gridType

        self.history = []
        
        self.generations = 0

        self.meanHistory = []
        


        self.griddler = self.gameDict["griddler"]
        
        self.evalRules = {"rows" : self.gameDict["rowRules"],
                          "cols" : self.gameDict["colRules"]}

        for r in range(self.gameDict["populationSize"]):
            if gridType:
                self.population.append(SlideGrid(self))
            else:
                self.population.append(SlideGridX(self))

        self.best = self.mostFit()


    def copy(self):
        p = Pop(self.gameDict)
        for a,b in zip(p.population, self.population):
            a.inheritFrom(b)
        p.generations = self.generations
        return p
        
    def __len__(self):
        return len(self.population)
    
    def __getitem__(self, key):
        
        return self.population[key].copy()
  
    def __setitem__(self, key, newvalue):
        
        self.population[key] = newvalue.copy()
    
    def selectAndReproduce(self):
        all([a.inheritFrom(b) for a,b in zip(
            self.population[(round(len(self.population) * self.gameDict["popSurvivalPct"])):],
            cycle(self.population[(round(len(self.population) * self.gameDict["popSurvivalPct"])):]))])
    
    def reproduceByFitness(self):
        newGen = []
        fitnessList = list([1/log(i.score) for i in self.population])
        Totalfitness = sum(fitnessList)
        normalizedFitness = [f/Totalfitness for f in fitnessList]
        
        for i in range(self.gameDict["populationSize"]):

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


    def mutate(self):
        for i in self.population:
            i.mutate()
       
    
    def popEvaluate(self):
        for p in self.population:
            p.evaluate()
    
    def popMean(self):
        return sum(list([p.score for p in self.population]))/len(self.population)
    
    def mostFit(self):
        best = self.population[0]
        for p in self.population[1:]:
            if p.score < best.score:
                best = p
        return best

    def iterate(self):
    
        self.popEvaluate()  
        self.best = self.mostFit()
        #print(self.best.score)
        self.history.append(self.best.score)
        self.reproduceByFitness()
        self.mutate()
        self.meanHistory.append(self.popMean())
        self.generations +=1