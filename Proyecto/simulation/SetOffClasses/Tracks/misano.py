from simulation.track import Track
from simulation.weather import Cardinals_Points
from simulation.track import Track_Type

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
            ("recta1", 265.5411, 263.9, Cardinals_Points.Southwest, Track_Type.Straight),
            ("curva1", 64.37376, 118.4, Cardinals_Points.West, Track_Type.Curve),
            ("recta2", 48.28032, 135, Cardinals_Points.West, Track_Type.Straight),
            ("curva2", 64.37376, 125.4, Cardinals_Points.South, Track_Type.Curve),
            ("recta3", 64.37376, 160.7, Cardinals_Points.South, Track_Type.Straight),
            ("curva3", 128.7475, 144.6, Cardinals_Points.West, Track_Type.Curve),
            ("recta4", 193.1213, 211.8, Cardinals_Points.West, Track_Type.Straight),
            ("curva4", 48.28032, 77.4, Cardinals_Points.Northwest, Track_Type.Curve),
            ("recta5", 48.28032, 93.7, Cardinals_Points.Northwest, Track_Type.Straight),
            ("curva5", 24.14016, 112.6, Cardinals_Points.Southeast, Track_Type.Curve),
            ("recta6", 72.42048, 130.8, Cardinals_Points.Southeast, Track_Type.Straight),
            ("curva6", 48.28032, 125.2, Cardinals_Points.Northwest, Track_Type.Curve),
            ("recta7", 579.3638, 275.2, Cardinals_Points.Northwest, Track_Type.Straight),
            ("curva7", 209.2147, 85.9, Cardinals_Points.Southeast, Track_Type.Curve),
            ("recta8", 225.3082, 237.1, Cardinals_Points.Southeast, Track_Type.Straight),
            ("curva8", 193.1213, 76.4, Cardinals_Points.Northwest, Track_Type.Curve),
            ("recta9", 547.177, 277.1, Cardinals_Points.Northwest, Track_Type.Straight),
            ("curva9", 32.18688, 244.5, Cardinals_Points.East, Track_Type.Curve),
            ("recta10", 225.3082, 265.6, Cardinals_Points.East, Track_Type.Straight),
            ("curva10", 96.56064, 160.6, Cardinals_Points.Southeast, Track_Type.Curve),
            ("recta11", 96.56064, 180.5, Cardinals_Points.Southeast, Track_Type.Straight),
            ("curva11", 32.18688, 144.3, Cardinals_Points.South, Track_Type.Curve),
            ("recta12", 112.6541, 98.6, Cardinals_Points.South, Track_Type.Straight),
            ("curva12", 96.56064, 67.4, Cardinals_Points.North, Track_Type.Curve),
            ("recta13", 128.7475, 163.0, Cardinals_Points.North, Track_Type.Straight),
            ("curva13", 64.37376, 141.9, Cardinals_Points.Northwest, Track_Type.Curve),
            ("recta14", 209.2147, 195.5, Cardinals_Points.Northwest, Track_Type.Straight),
            ("curva14", 32.18688, 114.3, Cardinals_Points.Southwest, Track_Type.Curve),
            ("recta15", 265.5411, 263.9, Cardinals_Points.Southwest, Track_Type.Straight)
            ]