from simulation.track import Track
from simulation.weather import CardinalsPoints
from simulation.track import SectionType


class Misano(Track):
    def __init__(self):
        """
        Posición 0: Nombre de la Sección
        Posición 1: Longitud de la sección en metros
        Posición 2: Velocidad Máxima permisible de la sección
        Posición 3: Punto Cardinal hacia donde está orientada la sección
        Posición 4: Tipo de Sección
        Posición 5: Es Pit Line
        """
        sections = [
            ("recta1", 265.5411, 263.9, CardinalsPoints.Southwest, SectionType.Straight, True),
            ("curva1", 64.37376, 118.4, CardinalsPoints.West, SectionType.Curve, True),
            ("recta2", 48.28032, 135, CardinalsPoints.West, SectionType.Straight, True),
            ("curva2", 64.37376, 125.4, CardinalsPoints.South, SectionType.Curve, True),
            ("recta3", 64.37376, 160.7, CardinalsPoints.South, SectionType.Straight, True),
            ("curva3", 128.7475, 144.6, CardinalsPoints.West, SectionType.Curve, True),
            ("recta4", 193.1213, 211.8, CardinalsPoints.West, SectionType.Straight, False),
            ("curva4", 48.28032, 77.4, CardinalsPoints.Northwest, SectionType.Curve, False),
            ("recta5", 48.28032, 93.7, CardinalsPoints.Northwest, SectionType.Straight, False),
            ("curva5", 24.14016, 112.6, CardinalsPoints.Southeast, SectionType.Curve, False),
            ("recta6", 72.42048, 130.8, CardinalsPoints.Southeast, SectionType.Straight, False),
            ("curva6", 48.28032, 125.2, CardinalsPoints.Northwest, SectionType.Curve, False),
            ("recta7", 579.3638, 275.2, CardinalsPoints.Northwest, SectionType.Straight, False),
            ("curva7", 209.2147, 85.9, CardinalsPoints.Southeast, SectionType.Curve, False),
            ("recta8", 225.3082, 237.1, CardinalsPoints.Southeast, SectionType.Straight, False),
            ("curva8", 193.1213, 76.4, CardinalsPoints.Northwest, SectionType.Curve, False),
            ("recta9", 547.177, 277.1, CardinalsPoints.Northwest, SectionType.Straight, False),
            ("curva9", 32.18688, 244.5, CardinalsPoints.East, SectionType.Curve, False),
            ("recta10", 225.3082, 265.6, CardinalsPoints.East, SectionType.Straight, False),
            ("curva10", 96.56064, 160.6, CardinalsPoints.Southeast, SectionType.Curve, False),
            ("recta11", 96.56064, 180.5, CardinalsPoints.Southeast, SectionType.Straight, False),
            ("curva11", 32.18688, 144.3, CardinalsPoints.South, SectionType.Curve, False),
            ("recta12", 112.6541, 98.6, CardinalsPoints.South, SectionType.Straight, False),
            ("curva12", 96.56064, 67.4, CardinalsPoints.North, SectionType.Curve, False),
            ("recta13", 128.7475, 163.0, CardinalsPoints.North, SectionType.Straight, False),
            ("curva13", 64.37376, 141.9, CardinalsPoints.Northwest, SectionType.Curve, False),
            ("recta14", 209.2147, 195.5, CardinalsPoints.Northwest, SectionType.Straight, False),
            ("curva14", 32.18688, 114.3, CardinalsPoints.Southwest, SectionType.Curve, True),
            ("recta15", 265.5411, 263.9, CardinalsPoints.Southwest, SectionType.Straight, True)
        ]
        super().__init__("Misano", 4226, sections)
