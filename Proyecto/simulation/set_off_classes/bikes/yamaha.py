from simulation.bike import Bike
from compilation.ast.nodes import Node


class Yamaha(Bike):
    def __init__(self, brand="Yamaha YZR M1 2021", max_speed=340, weight=157, node: Node = None):
        super().__init__(brand, max_speed, weight, node)
