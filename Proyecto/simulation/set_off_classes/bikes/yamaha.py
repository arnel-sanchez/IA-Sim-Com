from simulation.bike import Bike


class Yamaha(Bike):
    def __init__(self):
        super().__init__("Yamaha", "YZR M1 2021", 340, 157)
