from simulation.bike import Bike

class Yamaha(Bike):
    def __init__(self):
        self.brand = "Yamaha YZR M1 2021"
        self.max_speed = 340
        self.weight = 157