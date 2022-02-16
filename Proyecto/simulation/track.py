from enum import Enum
from random import uniform, normalvariate, randint

from simulation.weather import CardinalsPoints


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

    def __repr__(self):
        return "{} {} {} {} {} {}".format(self.name, self.length, self.max_speed, self.orientation, self.type,
                                          self.pit_line)


class Track:
    def __init__(self, name: str, length: float, sections: [Section]):
        self.name = name
        self.length = length
        self.sections = sections

    def reorder(self):
        for i in range(len(self.sections)):
            for j in range(i, len(self.sections)):
                if self.sections[i].orientation != self.sections[j].orientation or \
                        self.sections[i].type != self.sections[j].type:
                    continue
                prob = uniform(0, 2)
                if prob < 1:
                    continue
                section = self.sections[i]
                self.sections[i] = self.sections[j]
                self.sections[j] = section
                name = self.sections[i].name
                self.sections[i].name = self.sections[j].name
                self.sections[j].name = name


def track_generator():
    curve = False
    i = 1
    start_orientation = orientation_generator()
    orientation = start_orientation
    sections = []
    total_length = 0
    opposite = False
    while True:
        if not curve:
            name = "recta{}".format(i)
            length = normal(100, 1000)
            max_speed = normal(90, 350)
            section_type = SectionType.Straight
            pit_line = False###
        else:
            name = "curva{}".format(i)
            length = normal(50, 210)
            max_speed = normal(70, 240)
            while True:
                orientation = orientation_generator(orientation)
                diff = abs(orientation.value - start_orientation.value)
                if not opposite or 1 < diff < 7:
                    break
            if abs(orientation.value - start_orientation.value) == 4:
                opposite = True
            section_type = SectionType.Curve
            pit_line = False###
        sections.append(Section(name, length, max_speed, orientation, section_type, pit_line))
        total_length += length
        curve = not curve
        if 2000 < total_length:
            if total_length > 3500:
                curve = True
                i = 1
                orientation = start_orientation
                sections = [sections[0]]
                total_length = sections[0].length
            elif start_orientation != orientation and uniform(0, 1) < 0.3:
                break
    return Track("Random Track", length, sections)


def normal(a, b):
    return normalvariate((a + b) / 2, 100)


def orientation_generator(orientation: CardinalsPoints = None):
    if orientation is None:
        return CardinalsPoints(randint(0, 7))
    value = orientation.value
    prob = uniform(0, 1)
    if prob < 0.1:
        value -= 2
    elif prob < 0.3:
        value += 2
    elif prob < 0.5:
        value -= 1
    else:
        value += 1
    if value < 0:
        value += 8
    elif value > 7:
        value -= 8
    return CardinalsPoints(value)


track_generator()