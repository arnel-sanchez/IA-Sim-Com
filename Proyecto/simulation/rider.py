from simulation.bike import Bike

class Rider:
    def __init__(self, name, cornering, step_by_line):
        self.name = name
        self.cornering = cornering
        self.step_by_line = step_by_line
        self.probability_of_falling_off_the_motorcycle = 0.000001

    def assign_bike(self, bike: Bike,probability_of_falling_off_the_motorcycle):
        self.bike = bike
        self.probability_of_falling_off_the_motorcycle = probability_of_falling_off_the_motorcycle

    def print(self):
        print("Piloto: {}".format(self.name))
