from simulation.rider import Rider


class CrewChief:
    def __init__(self, name, aggressiveness, rider: Rider = None):
        self.name = name
        self.rider = rider

    def assign_rider(self, rider: Rider):
        self.rider = rider

    def print(self):
        print("Jefe Tecnico: {}".format(self.name))