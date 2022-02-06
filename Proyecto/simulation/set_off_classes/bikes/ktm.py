from simulation.bike import Bike
from compilation.ast.nodes import Node


class KTM(Bike):
    def __init__(self, brand="KTM RC16 2021", max_speed=362.4, weight=157, node: Node = None):
        super().__init__(brand, max_speed, weight, node)
