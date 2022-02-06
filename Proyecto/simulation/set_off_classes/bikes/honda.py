from simulation.bike import Bike
from compilation.ast.nodes import Node


class Honda(Bike):
    def __init__(self, brand="Honda RC213V 2021", max_speed=355, weight=160, node: Node = None):
        super().__init__(brand, max_speed, weight, node)
