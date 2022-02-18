from simulation.track import Track, Section, SectionType
from simulation.weather import CardinalsPoints


class Misano(Track):
    def __init__(self):
        """
        Posición 0: Nombre de la Sección
        Posición 1: Longitud de la sección en metros
        Posición 2: Velocidad Máxima permisible de la sección
        Posición 3: Punto Cardinal hacia donde está orientada la sección
        Posición 4: Tipo de Sección
        Posición 5: Es Pit Line
        Posición 6: Longitud de Pit Line
        """
        sections = [
            Section("recta1", 265.5411, 263.9, CardinalsPoints.Southwest, SectionType.Straight, True, 293.61),
            Section("curva1", 64.37376, 118.4, CardinalsPoints.West, SectionType.Curve, True, 75.41),
            Section("recta2", 48.28032, 135, CardinalsPoints.West, SectionType.Straight, True, 29.18),
            Section("curva2", 64.37376, 125.4, CardinalsPoints.South, SectionType.Curve, True, 53.11),
            Section("recta3", 64.37376, 160.7, CardinalsPoints.South, SectionType.Straight, True, 34.88),
            Section("curva3", 128.7475, 144.6, CardinalsPoints.West, SectionType.Curve, True, 113.71),
            Section("recta4", 193.1213, 211.8, CardinalsPoints.West, SectionType.Straight, False, 0),
            Section("curva4", 48.28032, 77.4, CardinalsPoints.Northwest, SectionType.Curve, False, 0),
            Section("recta5", 48.28032, 93.7, CardinalsPoints.Northwest, SectionType.Straight, False, 0),
            Section("curva5", 24.14016, 112.6, CardinalsPoints.Southeast, SectionType.Curve, False, 0),
            Section("recta6", 72.42048, 130.8, CardinalsPoints.Southeast, SectionType.Straight, False, 0),
            Section("curva6", 48.28032, 125.2, CardinalsPoints.Northwest, SectionType.Curve, False, 0),
            Section("recta7", 579.3638, 275.2, CardinalsPoints.Northwest, SectionType.Straight, False, 0),
            Section("curva7", 209.2147, 85.9, CardinalsPoints.Southeast, SectionType.Curve, False, 0),
            Section("recta8", 225.3082, 237.1, CardinalsPoints.Southeast, SectionType.Straight, False, 0),
            Section("curva8", 193.1213, 76.4, CardinalsPoints.Northwest, SectionType.Curve, False, 0),
            Section("recta9", 547.177, 277.1, CardinalsPoints.Northwest, SectionType.Straight, False, 0),
            Section("curva9", 32.18688, 244.5, CardinalsPoints.East, SectionType.Curve, False, 0),
            Section("recta10", 225.3082, 265.6, CardinalsPoints.East, SectionType.Straight, False, 0),
            Section("curva10", 96.56064, 160.6, CardinalsPoints.Southeast, SectionType.Curve, False, 0),
            Section("recta11", 96.56064, 180.5, CardinalsPoints.Southeast, SectionType.Straight, False, 0),
            Section("curva11", 32.18688, 144.3, CardinalsPoints.South, SectionType.Curve, False, 0),
            Section("recta12", 112.6541, 98.6, CardinalsPoints.South, SectionType.Straight, False, 0),
            Section("curva12", 96.56064, 67.4, CardinalsPoints.North, SectionType.Curve, False, 0),
            Section("recta13", 128.7475, 163.0, CardinalsPoints.North, SectionType.Straight, False, 0),
            Section("curva13", 64.37376, 141.9, CardinalsPoints.Northwest, SectionType.Curve, False, 0),
            Section("recta14", 209.2147, 195.5, CardinalsPoints.Northwest, SectionType.Straight, False, 0),
            Section("curva14", 32.18688, 114.3, CardinalsPoints.Southwest, SectionType.Curve, True, 78.18),
            Section("recta15", 265.5411, 263.9, CardinalsPoints.Southwest, SectionType.Straight, True, 216.7)
        ]
        super().__init__("Misano", 4226, sections)
