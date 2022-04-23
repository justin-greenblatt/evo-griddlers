from Gui import Gui

class ExperimentRunner:
    def __init__(self, experimentSpecies, parameters):
        self.experimentSpecies = experimentSpecies
        self.parameters = parameters
        self.gui = Gui(self.parameters)


    def run(self):

        for i in range(self.parameters["generations"]):
            for s in self.experimentSpecies:
                s.iterate()
            self.gui.printOut(self.experimentSpecies)
        self.gui.end(self.experimentSpecies)
        
    