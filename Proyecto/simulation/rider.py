

class Rider:
    def __init__(self, name, cornering, step_by_line, probability_of_falling_off_the_bike=1, independence=1,
                 expertise=1, aggressiveness=8):
        self.name = name
        self.cornering = cornering
        self.step_by_line = step_by_line
        self.probability_of_falling_off_the_bike = probability_of_falling_off_the_bike / 10000
        self.independence = independence / 100
        self.expertise = expertise / 1000
        self.aggressiveness = aggressiveness / 100
