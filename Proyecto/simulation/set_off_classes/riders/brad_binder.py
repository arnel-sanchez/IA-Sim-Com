from simulation.rider import Rider


class Binder(Rider):
    def __init__(self, name="Brad Binder", cornering=8, step_by_line=6):
        super().__init__(name, cornering, step_by_line)
