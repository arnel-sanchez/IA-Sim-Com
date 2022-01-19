from enum import Enum

class Tires(Enum):
    Slick_Soft = 0
    Slick_Medium = 1
    Slick_Hard = 2
    Rain_Soft = 3
    Rain_Medium = 4


class Bike:
    def __init__(self, brand, max_speed, weight, tires : Tires, brakes = 5, chassis_stiffness = 8):
        self.brand = brand
        self.max_speed = max_speed
        self.weight = weight
        self.tires = tires
        self.brakes = brakes
        self.chassis_stiffness = chassis_stiffness
        self.acceleration = 69.444
        self.probability_of_the_motorcycle_breaking_down = 0.000001
        self.probability_of_exploding_tires = 0.000001

    def change_tires(self, tires: Tires):
        self.tires = tires

    def change_chassis_stiffness(self, chassis_stiffness):
        self.chassis_stiffness = chassis_stiffness

    def change_brakes(self, brakes):
        self.brakes = brakes

    def print(self):
        print("Motocicleta: {}".format(self.brand))
