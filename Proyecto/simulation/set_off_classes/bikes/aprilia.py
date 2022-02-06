from simulation.bike import Bike
from compilation.ast.nodes import Node


class Aprilia(Bike):
    def __init__(self, brand="Aprilia RS-GP 2021", max_speed=357.6, weight=160, node: Node = None):
        super().__init__(brand, max_speed, weight, node)
