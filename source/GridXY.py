from sys import exit
from math import sqrt, log
from SlideGrid import SlideGrid
from random import choice, random, randint, choices
from Slide import Slide
import regex
from itertools import chain
from Resolver import Resolver


class GridXY(SlideGrid):
    def __init__(self, population):
        super().__init__(population)

        colSlides = []

        for bl in self.param["colRules"]:
            colSlides.append(Slide(bl, self.param["cols"]))
        
        self.colSlides = colSlides
        self.resolver = Resolver(self)
        self.evaluate()

    def inheritFrom(self, other):
        
        super().inheritFrom(other)

        for mySlide, parentSlide in zip(self.colSlides, other.colSlides):
            mySlide.copySlideState(parentSlide)
        self.resolver = other.resolver
    
    def copy(self):

        g = GridXY(self.population)
        g.inheritFrom(self)
        return g

    def locRows(self,i,j):
        return str(self.grid[i])[j]

    def locCols(self,i,j):
        return str(self.colSlides[j])[i]


    def colsFromColSlides(self):
        
        return [str(c) for c in self.colSlides]

    def rowsFromColSlides(self):
        return [ "".join(list([str(c)[a] for c in self.colSlides])) for a in range(len(self.grid))]


    def evaluate(self):

        self.levenshtein = list(         
            [r.match(s).fuzzy_counts[0] if r.match(s) != None else self.param["noMatchPenalty"] for r,s in 
                   zip(self.population.griddler.colRules, self.cols())])    
        
        self.colsLevenshtein = list(         
            [r.match(s).fuzzy_counts[0] if r.match(s) != None else self.param["noMatchPenalty"] for r,s in 
                   zip(self.population.griddler.rowRules, self.rowsFromColSlides())])

        self.score = self.resolve()

    def resolve(self):
        self.resScore = self.resolver.evaluate()
        if self.resScore == 0:
            print("Yeeeeeeeeeeeeessssssss")
            self.resolver.printEval()
            exit()

        rowL = sum(chain(self.levenshtein))
        colL = sum(chain(self.colsLevenshtein))
        stage = self.population.generations / self.param["generations"]
        if stage < 0.4:
            return rowL
        elif stage < 0.8:
            return colL
        else
            return  


 
    def mutate(self):
        if self.mutable:
            
            if random() < self.param["mutationRate"]:

                if random() < 0.5:
                
                    totalMutability = sum(list([len(s.zeros) for s in self.grid if s.mutable]))
                    
                    slideToMutate = choices([s for s in self.grid if s.mutable],
                                    weights = [len(s.zeros) for s in self.grid if s.mutable], k = 1)[0]
                    
                    slideToMutate.mutate()

                else:
                    
                    totalMutability = sum(list([len(s.zeros) for s in self.colSlides if s.mutable]))
                    
                    slideToMutate = choices([s for s in self.colSlides if s.mutable],
                                    weights = [len(s.zeros) for s in self.colSlides if s.mutable], k = 1)[0]
                    
                    slideToMutate.mutate()
        if random() < self.param["resolverMutationRate"]:
            self.resolver.mutate()

    def breed(self, other, resource = None):
        
        if not resource:
            resource = self.copy()
        
        else:
            resource.inheritFrom(self)
        mate = other.copy()
        resource.crossover(mate)

        return resource    

    def crossover(self, other):###########INFINIT LOOP
        super().crossover(other)
        crossCols = []
        for i in range(round(self.param["crossoverPct"]*self.param["cols"])):
            index = randint(0, len(self.colSlides)-1)
            while index in crossCols:
                index = randint(0, len(self.colSlides)-1)
            crossCols.append(index)
            give = self.colSlides[index].copy()        
            self.colSlides[index].copySlideState(other.colSlides[index])
            other.colSlides[index] = give


    def graphicRowSlides(self):

        outText = ""
        colors = (chr(0x1f7e9),chr(0x1f7e5))
        testLine = ("  " * (self.population.griddler.maxRows + 1)) + ' '
        if self.sex:
            for h in self.levenshtein:
                if h == 0:
                    testLine += colors[0]
                else:
                    testLine += colors[1]
        outText += testLine + '\n'
        for n,i in enumerate(self.grid):
           
            line = str(i)
            graphicLine = "".join(list([self.param["colors"][int(a)] for a in line]))
            self.population.griddler.printRow(n)
            if self.sex:
                outText += colors[0]
            outText += graphicLine + '\n'


    def graphicColSlides(self):
        
    def printMe(self):
        
        self.evaluate()
        self.population.griddler.printCols()
        colors = (chr(0x1f7e9),chr(0x1f7e5))
        testLine = ("  " * (self.population.griddler.maxRows + 1)) + ' '
        if self.sex:
            for h in self.levenshtein:
                if h == 0:
                    testLine += colors[0]
                else:
                    testLine += colors[1]
        print(testLine)
        for n,i in enumerate(self.grid):
           
            line = str(i)
            graphicLine = "".join(list([self.param["colors"][int(a)] for a in line]))
            self.population.griddler.printRow(n)
            if self.sex:
                print(colors[0], end = '')
            print(graphicLine)



        print('\n\n')
        self.population.griddler.printCols()

        testLine = ("  " * (self.population.griddler.maxRows + 1)) + ' ' 
        if self.sex:
            for h in self.levenshtein:
                testLine += colors[0]
        print(testLine)

        for n,(edit, row) in enumerate(zip(self.colsLevenshtein, self.rowsFromColSlides())):
            self.population.griddler.printRow(n)
            if edit == 0:
                print(colors[0], end = '')
            else:
                print(colors[1], end = '')

            graphicLine = "".join(list([self.param["colors"][int(a)] for a in row]))            
            print(graphicLine)