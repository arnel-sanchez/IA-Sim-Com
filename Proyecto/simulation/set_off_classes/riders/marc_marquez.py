from simulation.rider import Rider


class Marquez(Rider):
    def __init__(self, name="Marc Marquez", cornering=10, step_by_line=9):
        super().__init__(name, cornering, step_by_line)
