from simulation.bike import Bike
from compilation.ast.nodes import Node


class Ducati(Bike):
    def __init__(self, brand="Ducati Desmocedici 2021", max_speed=362.4, weight=157, node: Node = None):
        super().__init__(brand, max_speed, weight, node)
