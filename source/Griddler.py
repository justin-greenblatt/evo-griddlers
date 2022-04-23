from sys import exit
import regex

class Griddler:

    def __init__(self, directory, maxSubs = 5):
        
        self.rows = []
        self.cols = []
        
        try:
            handler = open(directory,'r')
        except Exception as e:
            print("Griddler problem input not valid")
            exit()
        
        colsFlag = False
        for l in handler:
            t = l
            if not t.strip():
                colsFlag = True
            if not colsFlag:

                self.rows.append(list([(int(b) ,'1') for b in l.split()]))
            else:
                if t.strip():
                    self.cols.append(list([(int(b) ,'1') for b in l.split()]))
        
        self.allBlocks = self.rows + self.cols

        self.size = (len(self.rows), len(self.cols))
        
        self.maxRows = max(list([len(c) for c in self.rows]))
        
        self.maxCols = max(list([len(c) for c in self.cols]))

        self.rowRules = [regex.compile("(?b)(?:^0*"+"0+".join([int(a)*b for a,b in r])+"0*$){s<=" + str(maxSubs) + "}") 
                         for r in self.rows]
        self.colRules = [regex.compile("(?b)(?:^0*"+"0+".join([int(a)*b for a,b in r])+"0*$){s<=" + str(maxSubs) + "}") 
                         for r in self.cols]
        self.allRules = self.rowRules + self.colRules
    def printCols(self):

        outText = ""
        for i in range(self.maxCols)[::-1]:
            outLine = ("  " * (self.maxRows + 1)) + ' '
            for j in self.cols:
                if len(j) > i:
                    b = j[i][0]
                    bs = str(b)
                    if len(bs) == 1:
                        outLine += bs + ' '
                    elif len(bs) == 2:
                        outLine += bs
                    else:
                        outLine += bs[0] + 'H'
                else:
                    outLine += "  "
            outText += outLine + '\n'
        outText += ("  " * (self.maxRows + 1))
        print(outText)

    def printRow(self,r):

        j = self.rows[r]
        outLine = ""
        for i in range(len(j)):
            if len(j) > i:
                        b = j[i][0]
                        bs = str(b)
                        if len(bs) == 1:
                            outLine += bs + ' '
                        elif len(bs) == 2:
                            outLine += bs
                        else:
                            outLine += bs[0] + 'H'
        while len(outLine) < self.maxRows*2:
            
            outLine = ' ' + outLine

        print(outLine, end =' ')

    def printAllRows(self):
        for r in range(len(self.rows)):
            self.printRow(r)
            print()

    def printRowsAndCols(self):
        self.printCols()
        self.printAllRows()