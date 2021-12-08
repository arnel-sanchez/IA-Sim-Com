from simulation.pilot import Pilot, default_pilots


class CrewChief:
    def __init__(self, name: str = "Jeremy Burgess", aggressiveness: int = 10, pilot: Pilot = None):
        self.name = name
        self.aggressiveness = aggressiveness
        self.pilot = pilot

    def assign_pilot(self, pilot: Pilot):
        self.pilot = pilot

    def print_crew_chief(self):
        print("Jefe Tecnico: {}".format(self.name))


def default_crew_chiefs():
    pilots = default_pilots()
    carchedi = CrewChief("Frankie Carchedi", 1, pilots["mir"])
    gabbarini = CrewChief("Christian Gabbarini", 2, pilots["bagnaia"])
    gubellini = CrewChief("Diego Gubellini", 3, pilots["quartararo"])
    hernandez = CrewChief("Santi Hernández", 4, pilots["marquez"])
    jimenez = CrewChief("Antonio Jiménez", 5, pilots["espargaro"])
    madrid = CrewChief("Andrés Madrid", 6, pilots["binder"])
    return {"carchedi": carchedi, "gabbarini": gabbarini, "gubellini": gubellini, "hernandez": hernandez,
            "jimenez": jimenez, "madrid": madrid}
