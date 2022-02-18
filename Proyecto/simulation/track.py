from enum import Enum
from random import uniform, randint

from simulation.weather import CardinalsPoints, opposite_direction


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
            length = value_generator(100, 1000)
            if i < 1 and length >= 500:
                length /= 2
            #max_speed = value_generator(90, 350)
            max_speed = 90 + (length - 100) / 3.4
            section_type = SectionType.Straight
            pit_line = False  ###
        else:
            name = "curva{}".format(i)
            length = value_generator(50, 210)
            max_speed = value_generator(70, 240)
            while True:
                orientation = orientation_generator(orientation)
                if opposite == opposite_direction(start_orientation, orientation):
                    break
            section_type = SectionType.Curve
            pit_line = False  ###
        sections.append(Section(name, length, max_speed, orientation, section_type, pit_line))
        i += 1
        total_length += length
        curve = not curve
        if 2000 < total_length:
            opposite = True
            if total_length > 3500:
                curve = True
                i = 1
                orientation = start_orientation
                sections = [sections[0]]
                total_length = sections[0].length
                opposite = False
            elif section_type == SectionType.Straight and opposite_direction(start_orientation, orientation) and \
                    uniform(0, 1) < 0.3:
                break
    return Track("Random Track", length, sections)


def value_generator(min_length, max_length):
    step = (max_length - min_length) / 10
    prob = uniform(0, 1)
    if prob < 0.50:
        length = uniform(min_length, min_length + step)
    elif prob < 0.60:
        length = uniform(min_length + step, min_length + 2 * step)
    elif prob < 0.70:
        length = uniform(min_length + 2 * step, min_length + 3 * step)
    elif prob < 0.80:
        length = uniform(min_length + 3 * step, min_length + 4 * step)
    elif prob < 0.85:
        length = uniform(min_length + step, min_length + 2 * step)
    elif prob < 0.90:
        length = uniform(min_length + 2 * step, min_length + 3 * step)
    elif prob < 0.94:
        length = uniform(min_length + 3 * step, min_length + 4 * step)
    elif prob < 0.97:
        length = uniform(min_length + 2 * step, min_length + 3 * step)
    elif prob < 0.99:
        length = uniform(min_length + 3 * step, min_length + 4 * step)
    else:
        length = uniform(min_length + 4 * step, max_length)
    return round(length, 5)


def orientation_generator(orientation: CardinalsPoints = None):
    if orientation is None:
        return CardinalsPoints(randint(0, 7))
    value = orientation.value
    prob = uniform(0, 1)
    if prob < 0.1:
        value -= 2
    elif prob < 0.3:
        value += 2
    elif prob < 0.6:
        value -= 1
    else:
        value += 1
    if value < 0:
        value += 8
    elif value > 7:
        value -= 8
    return CardinalsPoints(value)


track_generator()