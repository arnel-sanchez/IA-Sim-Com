from simulation.bike import Bike


class Rider:
    def __init__(self, name, cornering, step_by_line, probability_of_falling_off_the_bike = 1, aggressiveness = 1, bike = None, independence = 1):
        self.name = name
        self.cornering = cornering
        self.step_by_line = step_by_line
        self.probability_of_falling_off_the_bike = probability_of_falling_off_the_bike/1000000
        self.aggressiveness = aggressiveness/1000
        self.bike = bike
        self.independence = independence/1000000

    def assign_bike(self, bike: Bike, probability_of_falling_off_the_bike):
        self.bike = bike
        self.probability_of_falling_off_the_bike = probability_of_falling_off_the_bike

    def print(self):
        print("Piloto: {}".format(self.name))
