from simulation.rider import Rider
from simulation.bike import Bike
from enum import Enum

class Agent:
    def __init__(self, rider: Rider, bike: Bike):
        self.rider = rider
        self.bike = bike
        self.speed = 0
        self.aceleration = 0
        self.time_lap = 0

    def print():
        return

class Agent_actions(Enum):
    Speed_up = 0
    Brake = 1
    Bend = 2
    Go_to_the_pits = 3
    #Advance = 4