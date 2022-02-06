from simulation.rider import Rider


class Espargaro(Rider):
    def __init__(self, name="Aleix Espargaro", cornering=7, step_by_line=6):
        super().__init__(name, cornering, step_by_line)
