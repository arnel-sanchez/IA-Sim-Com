from simulation.rider import Rider, default_riders


class CrewChief:
    def __init__(self, name: str = "Jeremy Burgess", aggressiveness: int = 10, rider: Rider = None):
        self.name = name
        self.aggressiveness = aggressiveness
        self.rider = rider

    def assign_rider(self, rider: Rider):
        self.rider = rider

    def print_crew_chief(self):
        print("Jefe Tecnico: {}".format(self.name))


def default_crew_chiefs():
    riders = default_riders()
    carchedi = CrewChief("Frankie Carchedi", 1, riders["mir"])
    gabbarini = CrewChief("Christian Gabbarini", 2, riders["bagnaia"])
    gubellini = CrewChief("Diego Gubellini", 3, riders["quartararo"])
    hernandez = CrewChief("Santi Hernandez", 4, riders["marquez"])
    jimenez = CrewChief("Antonio Jimenez", 5, riders["espargaro"])
    madrid = CrewChief("Andres Madrid", 6, riders["binder"])
    return {"carchedi": carchedi, "gabbarini": gabbarini, "gubellini": gubellini, "hernandez": hernandez,
            "jimenez": jimenez, "madrid": madrid}
