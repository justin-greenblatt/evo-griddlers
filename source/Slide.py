from random import choice, choices, randint
from copy import deepcopy

class Slide:
    def __init__(self,blockList,arrayLength):

        spaces = ['^']
        self.arrayLength = arrayLength
        freeSpace = arrayLength
        self.mutable = False
        self.blockList = blockList
        
        if blockList != None and blockList != []:

            if blockList[0][0] != arrayLength:
                self.mutable = True
            

            for b in blockList[:-1]:
                freeSpace -= b[0]
                spaces.append('0')
                freeSpace -= 1

            freeSpace -= blockList[-1][0]

        spaces.append('$')
        
        for i in range(freeSpace):
            r = randint(0, len(spaces) - 1)
            spaceValue = spaces[r]
            if spaces[r].startswith('^'):
                spaces[r] = spaceValue + '0'
            else:
                spaces[r] = '0'+ spaceValue

        self.zeros = spaces


    def copySlideState(self, other):
        self.zeros = deepcopy(other.zeros)
    

    def copy(self):
        s = Slide(self.blockList, self.arrayLength)
        s.copySlideState(self)
        return s

    def mutate(self):
        
        if self.mutable:
            
            realScope = [z for z in self.zeros if "^" != z and "0" != z and "$" != z]

            self.mutability = len(realScope)

            ra = randint(0,len(self.zeros) -1)

            if len(realScope) > 0:

                while self.zeros[ra] not in realScope:
                    
                    ra = randint(0,len(self.zeros) -1)

                rb = ra + randint(-1,1)
            
                while rb == ra or rb < 0 or rb > (len(self.zeros) -1):
                    rb = ra + randint(-1,1)
                    
                if self.zeros[ra].endswith('$'):

                    self.zeros[ra] = self.zeros[ra][1:]
                else:
                    self.zeros[ra] = self.zeros[ra][:-1]

                if self.zeros[rb].endswith('$'):
                    self.zeros[rb] =  "0" + self.zeros[rb]
                else:
                    self.zeros[rb] = self.zeros[rb] + "0"
            
    def __str__(self):
        
        out = self.zeros[0].replace('^','')
        end = self.zeros[-1].replace('$','')
        inbetweeners = zip([b*n for n,b in self.blockList],self.zeros[1:-1]+[end])
        for block,z in inbetweeners:
            out += block
            out += z
    
        return out