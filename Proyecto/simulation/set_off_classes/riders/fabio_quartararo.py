from simulation.rider import Rider

class Quartararo(Rider):
    def __init__(self):
        self.name = "Fabio Quartararo"
        self.cornering = 9
        self.step_by_line = 8