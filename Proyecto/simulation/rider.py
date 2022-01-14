from simulation.bike import Bike

class Rider:
    def __init__(self, name, skill, cornering, step_by_line):
        self.name = name
        self.skill = skill
        self.cornering = cornering
        self.step_by_line = step_by_line
        self.experience_with_the_bike = 0
        self.probability_of_falling_off_the_motorcycle = 0

    def assign_bike(self, bike: Bike, experience, probability_of_falling_off_the_motorcycle):
        self.bike = bike
        self.experience_with_the_bike = experience
        self.probability_of_falling_off_the_motorcycle = probability_of_falling_off_the_motorcycle

    def add_experience(self):
        self.experience_with_the_bike+=1

    def print(self):
        print("Piloto: {}".format(self.name))
