from simulation.track import Track
from simulation.weather import CardinalsPoints
from simulation.track import TrackType

class Misano(Track):
    def __init__(self):
        self.name = "Misano"
        self.length = 4226
        '''
        Posición 0: Nombre de la Sección
        Posición 1: Longitud de la sección en metros
        Posición 2: Velocidad Máxima permisible de la sección
        Posición 3: Punto Cardinal hacia donde está orientada la sección
        Posición 4: Tipo de Sección
        '''
        self.sections = [
            ("recta1", 265.5411, 263.9, CardinalsPoints.Southwest, TrackType.Straight),
            ("curva1", 64.37376, 118.4, CardinalsPoints.West, TrackType.Curve),
            ("recta2", 48.28032, 135, CardinalsPoints.West, TrackType.Straight),
            ("curva2", 64.37376, 125.4, CardinalsPoints.South, TrackType.Curve),
            ("recta3", 64.37376, 160.7, CardinalsPoints.South, TrackType.Straight),
            ("curva3", 128.7475, 144.6, CardinalsPoints.West, TrackType.Curve),
            ("recta4", 193.1213, 211.8, CardinalsPoints.West, TrackType.Straight),
            ("curva4", 48.28032, 77.4, CardinalsPoints.Northwest, TrackType.Curve),
            ("recta5", 48.28032, 93.7, CardinalsPoints.Northwest, TrackType.Straight),
            ("curva5", 24.14016, 112.6, CardinalsPoints.Southeast, TrackType.Curve),
            ("recta6", 72.42048, 130.8, CardinalsPoints.Southeast, TrackType.Straight),
            ("curva6", 48.28032, 125.2, CardinalsPoints.Northwest, TrackType.Curve),
            ("recta7", 579.3638, 275.2, CardinalsPoints.Northwest, TrackType.Straight),
            ("curva7", 209.2147, 85.9, CardinalsPoints.Southeast, TrackType.Curve),
            ("recta8", 225.3082, 237.1, CardinalsPoints.Southeast, TrackType.Straight),
            ("curva8", 193.1213, 76.4, CardinalsPoints.Northwest, TrackType.Curve),
            ("recta9", 547.177, 277.1, CardinalsPoints.Northwest, TrackType.Straight),
            ("curva9", 32.18688, 244.5, CardinalsPoints.East, TrackType.Curve),
            ("recta10", 225.3082, 265.6, CardinalsPoints.East, TrackType.Straight),
            ("curva10", 96.56064, 160.6, CardinalsPoints.Southeast, TrackType.Curve),
            ("recta11", 96.56064, 180.5, CardinalsPoints.Southeast, TrackType.Straight),
            ("curva11", 32.18688, 144.3, CardinalsPoints.South, TrackType.Curve),
            ("recta12", 112.6541, 98.6, CardinalsPoints.South, TrackType.Straight),
            ("curva12", 96.56064, 67.4, CardinalsPoints.North, TrackType.Curve),
            ("recta13", 128.7475, 163.0, CardinalsPoints.North, TrackType.Straight),
            ("curva13", 64.37376, 141.9, CardinalsPoints.Northwest, TrackType.Curve),
            ("recta14", 209.2147, 195.5, CardinalsPoints.Northwest, TrackType.Straight),
            ("curva14", 32.18688, 114.3, CardinalsPoints.Southwest, TrackType.Curve),
            ("recta15", 265.5411, 263.9, CardinalsPoints.Southwest, TrackType.Straight)
            ]