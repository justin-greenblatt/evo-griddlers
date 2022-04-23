from sys import exit
from math import sqrt, log
from SlideGrid import SlideGrid
from random import choice, random, randint, choices
from Slide import Slide
import regex
from itertools import chain
from Resolver import Resolver

class SlideGridX(SlideGrid):
    def __init__(self, population):

        self.sex = False
        self.population = population
        self.param = population.gameDict
        self.nRows = self.param["rows"]
        self.nCols = self.param["cols"]
        colSlides = []

        for bl in self.param["colRules"]:
            colSlides.append(Slide(bl, self.param["cols"]))
        self.colSlides = colSlides
        self.mutable = any(list(([s.mutable for s in colSlides])))
        self.evaluate() 
        

    def inheritFrom(self, other):

        for mySlide, parentSlide in zip(self.colSlides, other.colSlides):
            mySlide.copySlideState(parentSlide)

    
    def copy(self):

        g = SlideGridX(self.population)
        g.inheritFrom(self)
        return g

    def locCols(self,i,j):
        return str(self.colSlides[j])[i]

    def rowsFromColSlides(self):
        return [ "".join(list([str(c)[a] for c in self.colSlides])) for a in range(self.param["rows"])]

    def colsFromColSlides(self):
        
        return [str(c) for c in self.colSlides]

    def evaluate(self):
       
        self.colsLevenshtein = list(         
            [r.match(s).fuzzy_counts[0] if r.match(s) != None else self.param["noMatchPenalty"] for r,s in 
                   zip(self.population.griddler.rowRules, self.rowsFromColSlides())])

        self.score =  sum(self.colsLevenshtein)

    def loc(self,i,j):
        return self.rowsFromColSlides()[i][j]

    def mutate(self):

        if self.mutable:
            
            if random() < self.param["mutationRate"]:
                    
                    totalMutability = sum(list([len(s.zeros) for s in self.colSlides if s.mutable]))
                    
                    slideToMutate = choices([s for s in self.colSlides if s.mutable],
                                    weights = [len(s.zeros) for s in self.colSlides if s.mutable], k = 1)[0]
                    
                    slideToMutate.mutate()


    def breed(self, other, resource = None):
        
        if not resource:
            resource = self.copy()
        
        else:
            resource.inheritFrom(self)
        mate = other.copy()
        resource.crossover(mate)

        return resource    

    def crossover(self, other):###########INFINIT LOOP
        crossCols = []
        for i in range(round(self.param["crossoverPct"]*self.param["cols"])):
            index = randint(0, len(self.colSlides)-1)
            while index in crossCols:
                index = randint(0, len(self.colSlides)-1)
            crossCols.append(index)
            give = self.colSlides[index].copy()        
            self.colSlides[index].copySlideState(other.colSlides[index])
            other.colSlides[index] = give


    def graphicColSlides(self):

        colors = (chr(0x1f7e9),chr(0x1f7e5))
        outText = ""
        testLine = ("  " * (self.population.griddler.maxRows + 1)) + ' ' 
        
        for h in self.levenshtein:
            testLine += colors[0]
        
        outText += testLine

        for edit, row in zip(self.colsLevenshtein, self.rowsFromColSlides()):

            if edit == 0:
                print(colors[0], end = '')
            else:
                print(colors[1], end = '')

            graphicLine = "".join(list([self.param["colors"][int(a)] for a in row]))            
            outText += graphicLine
        
        return outText

    def printMe(self):

        colors = (chr(0x1f7e9),chr(0x1f7e5))
        self.population.griddler.printCols()

        testLine = ("  " * (self.population.griddler.maxRows + 1)) + ' '
        
        for h in self.colsLevenshtein:
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

    def guiRow(self,n):
    
        out = ""
        colors = self.population.gameDict["flagColors"]
        
        if n == 0:
            out += "  " 
            for h in range(self.population.gameDict["cols"]):
                out += colors[0]
        else:

            n -= 1
    
            if self.colsLevenshtein[n] == 0:
                out += colors[0]
            else:
                out += colors[1]
    
            out += "".join(list([self.param["colors"][int(a)] for a in self.rowsFromColSlides()[n]]))            
        
        return out

    def guiId(self, spacer = "    "):
        out = "COL_OPT|SCORE:{}|POP:{}".format(self.score, self.population.id)
        if len(out) < self.nCols * 2:
            while len(out) < self.nCols * 2:
                out += ' '
        elif len(out) > self.nCols * 2:
            while len(out) > self.nCols * 2:
                out = out[:-1]
        return out