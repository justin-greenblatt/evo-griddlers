from random import randint, random

class MutateMap:
    def __init__(self,dimensions,expressions, mutationRate, startState = None):
        self.rows = dimensions[0]
        self.cols = dimensions[1]
        self.expressions = expressions

        self.rowExpressions = self.expressions[:self.rows]
        self.colExpressions = self.expressions[self.rows:]

        self.generation = 0

        rowsSum = list([sum(list([b[0] for b in row])) for row in self.rowExpressions])
        colsSum = list([sum(list([b[0] for b in col])) for col in self.colExpressions])
        rowVals = [((rS - (self.rows - rS))**2) + (rS * (self.rows - rS)) for rS in rowsSum]
        colVals = [((cS - (self.cols - cS))**2) + (cS * (self.cols - cS)) for cS in colsSum]
        
        self.mutationRates = []

        for i in range(self.cols):
            for j in range(self.rows):
                val = ((colVals[i] * rowVals[j])/max(self.rows,self.cols)**4)*mutationRate
                self.mutationRates.append(val)
                print(str(val)[:5], end = ' ')
            print('*')

        self.slidesRow = list([sum(self.mutationRates[i * self.cols : (i + 1) * self.cols ]) for i in range(self.rows)])
        self.slidesCol = list([sum(self.mutationRates[i:len(self.mutationRates) - 1: self.cols]) for i in range(self.cols)])
        


    def mutate(self,grid):
        
        for  a,b in enumerate(self.mutationRates):
            
            if random() < b:
            
                randomMod = grid.string[a]
                
                while randomMod == grid.string[a]:
                    randomMod = grid.language[randint(0,len(grid.language) - 1)]

                grid.string = grid.string[:a] + randomMod + grid.string[a + 1:]

        return grid



