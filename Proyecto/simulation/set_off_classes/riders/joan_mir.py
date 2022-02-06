from simulation.rider import Rider


class Mir(Rider):
    def __init__(self, name="Joan Mir", cornering=8, step_by_line=8):
        super().__init__(name, cornering, step_by_line)
