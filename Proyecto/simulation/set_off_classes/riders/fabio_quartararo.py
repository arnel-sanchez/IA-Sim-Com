from simulation.rider import Rider


class Quartararo(Rider):
    def __init__(self, name="Fabio Quartararo", cornering=9, step_by_line=8):
        super().__init__(name, cornering, step_by_line)
