from simulation.motorcycle import Motorcycle, default_motorcycles


class Pilot:
    def __init__(self, name: str = "Valentino Rossi", aggressiveness: int = 10, motorcycle: Motorcycle = None):
        self.name = name
        self.aggressiveness = aggressiveness
        self.motorcycle = motorcycle

    def assign_motorcycle(self, motorcycle: Motorcycle):
        self.motorcycle = motorcycle

    def print_pilot(self):
        print("Piloto: {}".format(self.name))


def default_pilots():
    motorcycles = default_motorcycles()
    bagnaia = Pilot("Francesco Bagnaia", 1, motorcycles["ducati"])
    binder = Pilot("Brad Binder", 2, motorcycles["ktm"])
    espargaro = Pilot("Aleix Espargaro", 3, motorcycles["aprilia"])
    marquez = Pilot("Marc Marquez", 4, motorcycles["honda"])
    mir = Pilot("Joan Mir", 5, motorcycles["suzuki"])
    quartararo = Pilot("Fabio Quartararo", 6, motorcycles["yamaha"])
    return {"bagnaia": bagnaia, "binder": binder, "espargaro": espargaro, "marquez": marquez, "mir": mir,
            "quartararo": quartararo}
