from enum import Enum

from weather import CardinalsPoints


class SectionType(Enum):
    Curve = 0
    Straight = 1


class Section:
    def __init__(self, name: str, length: float, max_speed: float, orientation: CardinalsPoints,
                 section_type: SectionType, pit_line: bool):
        self.name = name
        self.length = length
        self.max_speed = max_speed
        self.orientation = orientation
        self.type = section_type
        self.pit_line = pit_line


class Track:
    def __init__(self, name: str, length: float, sections: [Section]):
        self.name = name
        self.length = length
        self.sections = sections
