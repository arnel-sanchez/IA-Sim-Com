from enum import Enum

class Track_Type(Enum):
    Curve = 0
    Straight = 1

class Track:
    def __init__(self, name, length, sections):
        self.name = name
        self.length = length
        self.sections = sections