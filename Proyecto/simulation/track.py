from enum import Enum
from random import uniform, normalvariate, randint

from simulation.weather import CardinalsPoints


class SectionType(Enum):
    Curve = 0
    Straight = 1


class PitSection(Enum):
    No = 0
    Start = 1
    Middle = 2
    End = 3


class Section:
    def __init__(self, name: str, length: float, max_speed: float, orientation: CardinalsPoints,
                 section_type: SectionType, pit_line: PitSection, pit_length: float):
        self.name = name
        self.length = length
        self.max_speed = max_speed
        self.orientation = orientation
        self.type = section_type
        self.pit_line = pit_line
        self.pit_length = pit_length

    def __repr__(self):
        return "{} {} {} {} {} {}".format(self.name, self.length, self.max_speed, self.orientation, self.type,
                                          self.pit_line)


class Track:
    def __init__(self, name: str, length: float, sections: [Section]):
        self.name = name
        self.length = length
        self.sections = sections

    def shuffle(self):
        self.name = "Shuffled " + self.name
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
    ranges = [(90, 140), (140, 180), (180, 220), (220, 250), (250, 280), (280, 300), (300, 320), (320, 335),
              (335, 350)]
    curve = False
    i = 0
    start_orientation = orientation_generator()
    orientation = start_orientation
    sections = []
    total_length = 0
    opposite = False
    while True:
        if curve:
            name = "curva{}".format(i)
            length = value_generator(50, 210)
            max_value = min(240.0, sections[-1].max_speed)
            max_speed = value_generator(70, max_value)
            while True:
                orientation = orientation_generator(orientation)
                if opposite == (abs(start_orientation.value - orientation.value) == 4):
                    break
            section_type = SectionType.Curve
            pit_length = length / 2
        else:
            i += 1
            name = "recta{}".format(i)
            if opposite:
                length = sections[0].length
                max_speed = sections[0].max_speed
            else:
                length = value_generator(100, 999)
                x = ranges[int(length / 100) - 1]
                max_speed = normalvariate((x[0] + x[1]) / 2, 10)
            section_type = SectionType.Straight
            pit_length = length
        if len(sections) == 4:
            pit_section = PitSection.End
        elif len(sections) < 5:
            pit_section = PitSection.Middle
        else:
            pit_section = PitSection.No
            pit_length = 0
        sections.append(Section(name, round(length, 2), round(max_speed, 2), orientation, section_type, pit_section,
                                round(pit_length, 2)))
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
            elif section_type == SectionType.Curve and abs(start_orientation.value - orientation.value) == 4 and \
                    uniform(0, 1) < 0.3:
                break
    count = len(sections) + 1
    j = int(count / 2)
    for i in range(count):
        section = sections[i]
        if section.type == SectionType.Straight:
            j += 1
            name = "recta{}".format(j)
        else:
            name = "curva{}".format(j)
        orientation = section.orientation.value + 4
        if orientation > 7:
            orientation -= 8
        if i == count - 2:
            pit_section = PitSection.Start
            pit_length = round(length / 2, 2)
        elif i == count - 1:
            pit_section = PitSection.Middle
            pit_length = length
        else:
            pit_section = PitSection.No
            pit_length = 0
        sections.append(Section(name, section.length, section.max_speed, CardinalsPoints(orientation), section.type,
                                pit_section, pit_length))
        total_length += length
    sections[0].length = round(sections[0].length / 2, 2)
    sections[-1].length = round(sections[-1].length / 2, 2)
    return Track("Random Track", round(total_length, 2), sections)


def value_generator(min_length, max_length):
    step = (max_length - min_length) / 10
    prob = uniform(0, 1)
    if prob < 0.50:
        value = uniform(min_length, min_length + step)
    elif prob < 0.60:
        value = uniform(min_length + step, min_length + 2 * step)
    elif prob < 0.70:
        value = uniform(min_length + 2 * step, min_length + 3 * step)
    elif prob < 0.80:
        value = uniform(min_length + 3 * step, min_length + 4 * step)
    elif prob < 0.85:
        value = uniform(min_length + step, min_length + 2 * step)
    elif prob < 0.90:
        value = uniform(min_length + 2 * step, min_length + 3 * step)
    elif prob < 0.94:
        value = uniform(min_length + 3 * step, min_length + 4 * step)
    elif prob < 0.97:
        value = uniform(min_length + 2 * step, min_length + 3 * step)
    elif prob < 0.99:
        value = uniform(min_length + 3 * step, min_length + 4 * step)
    else:
        value = uniform(min_length + 4 * step, max_length)
    return value


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
