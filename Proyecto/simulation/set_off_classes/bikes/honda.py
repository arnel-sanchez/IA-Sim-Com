from simulation.bike import Bike


class Honda(Bike):
    def __init__(self):
        super().__init__("Honda", "RC213V 2021", 355, 160)
