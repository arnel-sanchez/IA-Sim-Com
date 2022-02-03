from simulation.bike import Bike

class Honda(Bike):
    def __init__(self):
        self.brand = "Honda RC213V 2021"
        self.max_speed = 355
        self.weight = 160