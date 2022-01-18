from simulation.environment import Environment
from numpy.random import random
from numpy.random import randint

class Race:
    def __init__(self, laps, agents, environment: Environment):
        self.agents = agents
        self.environment = environment
        self.laps = laps
        self.current_lap = 0
        self.rank = agents

    def change_lap(self):
        self.current_lap+=1
        if self.current_lap == self.laps:
            print("\nCarrera terimnada\n")
            self.print_ranking()
            return True
        elif self.current_lap == self.laps-1:
            print("\nUltima vuelta\n")
            self.print_ranking()
            return False
        else:
            print("\nVuelta {}\n".format(self.current_lap))
            self.print_ranking()
            return False

    def print_ranking(self):
        i = 1
        for x in self.rank:
            print("{}: {}".format(i, x.rider.name))
            i+=1

    def ranking(self):
        self.agents.sort(key=lambda agent : agent.time_lap)

    def continuous_variable_generator(self):
        return random()

    def discrete_variable_generator(self):
        return randint(1, 10)