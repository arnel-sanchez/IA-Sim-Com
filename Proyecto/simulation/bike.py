from enum import Enum


class Tires(Enum):
    Slick_Soft = 0
    Slick_Medium = 1
    Slick_Hard = 2
    Rain_Soft = 3
    Rain_Medium = 4


class Bike:
    def __init__(self, brand, max_speed, weight, brakes, chassis_stiffness, tires : Tires = None):
        self.brand = brand
        self.max_speed = max_speed
        self.weight = weight
        self.tires = tires
        self.brakes = brakes
        self.chassis_stiffness = chassis_stiffness

    def change_tires(self, tires: Tires):
        self.tires = tires

    def change_chassis_stiffness(self, chassis_stiffness):
        self.chassis_stiffness = chassis_stiffness

    def change_brakes(self, brakes):
        self.brakes = brakes

    def print(self):
        print("Motocicleta: {}".format(self.brand))
