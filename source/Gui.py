from os import system

class Gui(object):
    """docstring for Gui"""
    def __init__(self, parameters):
        self.parameters = parameters

    def printOut(self,speciesGroups, spacer = "    "):
        
        system("clear")
        self.parameters["griddler"].printCols()
        
        for n in range(self.parameters["rows"] + 1):
            
            if n != 0:
                self.parameters["griddler"].printRow(n - 1)
            else: 
                print((self.parameters["griddler"].maxRows * "  ") + ' ', end = '')
            
            print(spacer.join(list([s.guiRow(n) for s in speciesGroups])))



        print((self.parameters["griddler"].maxRows * "  ") + ' ', end = '')    
        print("      ".join(list([s.guiId() for s in speciesGroups])))


    def end(self,speciesGroups):
        self.printOut(speciesGroups)
