from enum import Enum

from compilation.ast.specials import BikeNode
from simulation.environment import Environment
from ai.ai import edit_moto, call_ai


class Tires(Enum):
    Slick_Soft = 0
    Slick_Medium = 1
    Slick_Hard = 2
    Rain_Soft = 3
    Rain_Medium = 4


class Bike:
    def __init__(self, brand, model, max_speed, weight, node: BikeNode = None, brakes=5, chassis_stiffness=8,
                 probability_of_the_bike_breaking_down=1, probability_of_exploding_tires=1, tires=Tires.Slick_Medium):
        self.brand = brand
        self.model = model
        self.max_speed = max_speed
        self.weight = weight
        self.tires = tires
        self.brakes = brakes
        self.chassis_stiffness = chassis_stiffness
        self.probability_of_the_bike_breaking_down = probability_of_the_bike_breaking_down / 10000
        self.probability_of_exploding_tires = probability_of_exploding_tires / 10000
        self.node = node

    def select_configuration(self, environment: Environment):
        if self.node is None or len(self.node.funciones) == 0:
            edit_moto(environment)
            tires = call_ai("moto.py")
            self.change_tires(Tires[tires])
        else:
            self.node.refreshContext(self.__dict__, environment.weather.__dict__)
            self.node.funciones[0].eval([], self.node.nuevocontext)
            evaluation = self.node.nuevocontext.variables["tires"].value
            if evaluation <= 4:
                self.tires = Tires(evaluation)
            else:
                evaluation = 4
                self.tires = Tires(evaluation)

    def change_tires(self, tires: Tires):
        self.tires = tires

    def change_chassis_stiffness(self, chassis_stiffness):
        self.chassis_stiffness = chassis_stiffness

    def change_brakes(self, brakes):
        self.brakes = brakes
