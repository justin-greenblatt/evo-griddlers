from sys import exit
from os import system
import parameters
from random import randint, random, choice
from itertools import chain

class Resolver:

    def __init__(self, population):
        self.gameDict = population.gameDict
        self.population = population
        self.hostCol =  choice([a for b in self.population.colHostPopulations for a in b])
        self.hostRow =  choice([a for b in self.population.rowHostPopulations for a in b])
        self.rows = self.hostRow.param["rows"]
        self.cols = self.hostRow.param["cols"]
        self.string = "".join(list([str(randint(0,1)) for a in range(self.rows * self.cols)]))
        self.evaluate()
    
    def resolvedGrid(self):

        return  "".join(list([self.hostCol.loc(i,j) if self.loc(i,j) == '0' 
                else self.hostRow.loc(i,j) 
                for i in range(self.rows)
                for j in range(self.cols)]))

    def evaluate(self):
        

        myRows = [[[c.count('1'), '1'] for c in [self.resolvedGrid()[self.rows*i: self.rows*(i+1)].split('0')]] for i in range(self.rows)]         
        myCols = [[[c.count('1'), '1'] for c in [self.resolvedGrid()[i:len(self.resolvedGrid()):self.cols].split('0')]] for i in range(self.cols)]
        myRules = myRows + myCols
        evaluation = []
        identityCount = 0

        for a,b in zip(myRules, self.population.griddler.allBlocks):
        
            for c,d in zip(a,b):
        
                if c != d:
                    evaluation.append(1)
                else:
                    evaluation.append(0)
        
        self.evaluation = evaluation
        self.score = self.evaluation.count(1)

    def guiRow(self, n, spacer = "    "):

        out = ""

        if n == 0:
            out += "  "*(self.rows + 1)
            out += spacer
            for i in self.evaluation[self.rows:]:
                out += self.population.gameDict["flagColors"][i]
        else:
            n -= 1
            line = (self.string[self.rows*n: self.rows*(n+1)])
            out += "".join(list([self.hostRow.param["resolverColors"][int(a)] for a in line]))
            out += spacer
            out += self.population.gameDict["flagColors"][self.evaluation[n]]
            line = (self.resolvedGrid()[self.rows*n: self.rows*(n+1)])
            out +=  "".join(list([self.hostRow.param["colors"][int(a)] for a in line]))
        return out
            

    def guiId(self):

        out = "MASK|H1{}-{}|H2{}-{}".format(self.hostCol.__repr__()[-2:], self.hostCol.population.id,
                                         self.hostRow.__repr__()[-2:], self.hostRow.population.id)
        if len(out) < self.cols * 2:
            while len(out) < self.cols * 2:
                out += ' '
        elif len(out) > self.cols * 2:
            while len(out) > self.cols * 2:
                out = out[:-1]
        product = out + "    "
        out = "COMBINED|SCORE:{}|POP:{}".format(self.score, self.population.id)
        if len(out) < self.cols * 2:
            while len(out) < self.cols * 2:
                out += ' '
        elif len(out) > self.cols * 2:
            while len(out) > self.cols * 2:
                out = out[:-1]
        return product + out

    def printMe(self):
        print("MASK|{}|H1{}-{}|H2{}-{}".format(self.hostCol.__repr__()[-2:], self.hostCol.population.id,
                                         self.hostRow.__repr__()[-2:], self.hostRow.population.id))
        for i in range(self.rows):
            line = (self.string[self.rows*i: self.rows*(i+1)])
            graphicLine = "".join(list([self.hostRow.param["resolverColors"][int(a)] for a in line]))
            print(graphicLine)
        print('\n')


    def printEval(self):

        for i in range(self.rows):
            line = (self.resolvedGrid()[self.rows*i: self.rows*(i+1)])
            graphicLine = "".join(list([self.hostRow.param["colors"][int(a)] for a in line]))
            print(graphicLine)
        print('\n')

    
    def getRow(self,n):
        n %= self.rows
        return self.string[n*self.cols: (n+1)*(self.cols)]

    def getCol(self,n):
        n %= self.cols
        return self.string[n:len(self.string) -1: self.cols]
    
    def setRow(self, n, newRow):
        n %= self.rows
        self.string = self.string[:n*self.cols] +  newRow + self.string[(n+1)*(self.cols):] 
    
    def setLetter(self,n,letter):
        n %= len(self.string)
        self.string = self.string[:n] + letter + self.string[n+1:]

    def setCol(self,n,newCol):
        n %= self.cols
        for s,i in enumerate(range(n,len(self.string) - 1, self.cols)):
            self.setLetter(i,newCol[s])


    def mutate(self):
        r = randint(0, len(self.string) - 1)
        if self.string[r] == '0':
            self.setLetter(r, '1')
        else:
            self.setLetter(r, '0')

    def loc(self,i,j):
        return self.string[(i*self.rows) + j]


    def crossOver(self,mate):

        size = round(self.rows * self.gameDict["resolverCrossoverPct"])
        for i in range(size):

            rIndex = randint(0,self.rows -1)
            self.setRow(rIndex, mate.getRow(rIndex))

            cIndex = randint(0,self.cols -1)
            self.setCol(cIndex, mate.getCol(cIndex))
            

    def changeHost(self):
        if random() < self.gameDict["resolverHostSwap"]:
            if random() < 0.5:
                self.hostCol = choice([a for b in self.population.colHostPopulations for a in b])
            else: 
                self.hostRow = choice([a for b in self.population.rowHostPopulations for a in b])                


    def breed(self, other):
        new = Resolver(self.population)
        new.inheritFrom(self)
        new.crossOver(other)
        return new

    def inheritFrom(self, other):
        self.string == other.string

    def __eq__(self, other):
        return self.string == other.string

    def __lt__(self, other):
        return self.score < other.score