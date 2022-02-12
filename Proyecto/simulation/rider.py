from simulation.bike import Bike


class Rider:
    def __init__(self, name, cornering, step_by_line):
        self.name = name
        self.cornering = cornering
        self.step_by_line = step_by_line
        self.probability_of_falling_off_the_bike = 0.000001
        self.aggressiveness = 0.001
        self.bike = None

    def assign_bike(self, bike: Bike, probability_of_falling_off_the_bike):
        self.bike = bike
        self.probability_of_falling_off_the_bike = probability_of_falling_off_the_bike

    def print(self):
        print("Piloto: {}".format(self.name))
