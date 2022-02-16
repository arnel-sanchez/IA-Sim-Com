
class Rider:
    def __init__(self, name, turning_curves, driving_straight, probability_of_falling_off_the_bike=1, independence=1,
                 expertise=1, aggressiveness=8):
        self.name = name
        self.turning_curves = turning_curves
        self.driving_straight = driving_straight
        self.probability_of_falling_off_the_bike = probability_of_falling_off_the_bike / 10000
        self.independence = independence / 100
        self.expertise = expertise / 1000
        self.aggressiveness = aggressiveness / 100
