from simulation.rider import Rider


class Bagnaia(Rider):
    def __init__(self, name="Pecco Bagnaia", cornering=8, step_by_line=9):
        super().__init__(name, cornering, step_by_line)
