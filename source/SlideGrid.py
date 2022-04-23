from random import choice, random, randint, choices
from Slide import Slide
import regex

class SlideGrid:

    def __init__(self, population):

        self.sex = True
        self.population = population
        self.param = population.gameDict
        self.nRows = self.param["rows"]
        self.nCols = self.param["cols"]
    
        slides = []

        for bl in self.param["rowRules"]:
            slides.append(Slide(bl, self.param["rows"]))


        
        self.mutable = any(list(([s.mutable for s in slides])))
        
        self.grid = slides                

        self.levenshtein =  list(         
            [r.match(s).fuzzy_counts[0] if r.match(s) != None else self.param["noMatchPenalty"] for r,s in 
                   zip(self.population.griddler.colRules, self.cols())])    
        
        self.score = sum(self.levenshtein)

    def inheritFrom(self, other):
        
        for mySlide, parentSlide in zip(self.grid, other.grid):
            mySlide.copySlideState(parentSlide)

    def copy(self):
        g = SlideGrid(self.population)
        g.inheritFrom(self)
        return g

    def __eq__(self, other):
        for s,o in zip(self.grid, other.grid):
            if str(s) != str(o):
                return False
        return True

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        out = ""
        for s in self.grid:
            out += str(s)
            out += '\n'
        return out

    def strLong(self):
        return str(self).replace("\n", "")

    def __len__(self):
        return len(self.strLong())


    def cols(self):
        
        data = self.strLong()
        return [data[a:len(self):self.param["cols"]] for a in range(self.param["cols"])]

    def loc(self, i, j):
        return str(self.grid[i])[j]

    def mutate(self):
        if self.mutable:
            
            if random() < self.param["mutationRate"]:
                
                totalMutability = sum(list([len(s.zeros) for s in self.grid if s.mutable]))
                
                slideToMutate = choices([s for s in self.grid if s.mutable],
                                weights = [len(s.zeros) for s in self.grid if s.mutable], k = 1)[0]
                
                slideToMutate.mutate()


    def evaluate(self):

        self.levenshtein =  list(         
            [r.match(s).fuzzy_counts[0] if r.match(s) != None else self.param["noMatchPenalty"] for r,s in 
                   zip(self.population.griddler.colRules, self.cols())])    

        self.score = sum(self.levenshtein)

    def breed(self, other, resource = None):
        
        if not resource:
            resource = self.copy()
        
        else:
            resource.inheritFrom(self)
        mate = other.copy()
        resource.crossover(mate)

        return resource    

    def crossover(self, other):###########INFINIT LOOP
        crossRows = []
        for i in range(round(self.param["crossoverPct"]*self.param["rows"])):
            index = randint(0, len(self.grid)-1)
            while index in crossRows:
                index = randint(0, len(self.grid)-1)
            crossRows.append(index)
            give = self.grid[index].copy()        
            self.grid[index].copySlideState(other.grid[index])
            other.grid[index] = give

    def printMe(self):
        
        self.evaluate()
        self.population.griddler.printCols()
        colors = (chr(0x1f7e9),chr(0x1f7e5))
        testLine = "  " * (self.population.griddler.maxRows + 1)
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
        print('\n')

    def guiRow(self,n):
        
        out = ""
        colors = self.population.gameDict["flagColors"]
        if n == 0:
            out += "  "
            for l in self.levenshtein:
                if l == 0:
                    out += colors[0]
                else:
                    out += colors[1]

        else:
            n -= 1
            out += colors[0]
            out += "".join(list([self.param["colors"][int(a)] for a in str(self.grid[n])]))            
        return out


    def guiId(self, spacer = "    "):

        out = "ROW_OPT|SCORE:{}|POP:{}".format(self.score, self.population.id)
        if len(out) < self.nCols * 2:
            while len(out) < self.nCols * 2:
                out += ' '
        elif len(out) > self.nCols * 2:
            while len(out) > self.nCols * 2:
                out = out[:-1]
        return out