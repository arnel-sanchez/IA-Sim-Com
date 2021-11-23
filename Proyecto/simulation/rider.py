from simulation.motorcycle import Motorcycle, default_motorcycles


class Rider:
    def __init__(self, name: str = "Valentino Rossi", aggressiveness: int = 10, motorcycle: Motorcycle = None):
        self.name = name
        self.aggressiveness = aggressiveness
        self.motorcycle = motorcycle

    def assign_motorcycle(self, motorcycle: Motorcycle):
        self.motorcycle = motorcycle

    def print_rider(self):
        print("Piloto: {}".format(self.name))


def default_riders():
    motorcycles = default_motorcycles()
    bagnaia = Rider("Francesco Bagnaia", 1, motorcycles["ducati"])
    binder = Rider("Brad Binder", 2, motorcycles["ktm"])
    espargaro = Rider("Aleix Espargaró", 3, motorcycles["aprilia"])
    marquez = Rider("Marc Márquez", 4, motorcycles["honda"])
    mir = Rider("Joan Mir", 5, motorcycles["suzuki"])
    quartararo = Rider("Fabio Quartararo", 6, motorcycles["yamaha"])
    return {"bagnaia": bagnaia, "binder": binder, "espargaro": espargaro, "marquez": marquez, "mir": mir,
            "quartararo": quartararo}
