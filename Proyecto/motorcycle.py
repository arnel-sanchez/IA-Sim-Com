from enum import Enum


class Tyres(Enum):
    Slick_Soft = 0
    Slick_Medium = 1
    Slick_Hard = 2
    Rain_Soft = 3
    Rain_Medium = 4


class Motorcycle:
    def __init__(self, brand: str = "Yamaha", max_speed: int = 350, weight: int = 157, tyres: Tyres = None):
        self.brand = brand
        self.max_speed = max_speed
        self.weight = weight
        self.tyres = tyres

    def change_tires(self, tyres: Tyres):
        self.tyres = tyres

    def print_motorcycle(self):
        print("Motocicleta: {}".format(self.brand))


def default_motorcycles():
    aprilia = Motorcycle("Aprilia")
    ducati = Motorcycle("Ducati")
    honda = Motorcycle("Honda")
    ktm = Motorcycle("KTM")
    suzuki = Motorcycle("Suzuki")
    yamaha = Motorcycle("Yamaha")
    return {"aprilia": aprilia, "ducati": ducati, "honda": honda, "ktm": ktm, "suzuki": suzuki, "yamaha": yamaha}
