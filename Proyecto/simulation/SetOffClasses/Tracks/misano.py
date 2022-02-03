from simulation.track import Track
from simulation.weather import Cardinals_Points

class Misano(Track):
    def __init__(self):
        self.name = "Misano"
        self.length = 4226
        self.sections = [
            ("recta1", 265.5411, 263.9, Cardinals_Points.Southwest),
            ("curva1", 64.37376, 118.4, Cardinals_Points.West),
            ("recta2", 48.28032, 135, Cardinals_Points.West),
            ("curva2", 64.37376, 125.4, Cardinals_Points.South),
            ("recta3", 64.37376, 160.7, Cardinals_Points.South),
            ("curva3", 128.7475, 144.6, Cardinals_Points.West),
            ("recta4", 193.1213, 211.8, Cardinals_Points.West),
            ("curva4", 48.28032, 77.4, Cardinals_Points.Northwest),
            ("recta5", 48.28032, 93.7, Cardinals_Points.Northwest),
            ("curva5", 24.14016, 112.6, Cardinals_Points.Southeast),
            ("recta6", 72.42048, 130.8, Cardinals_Points.Southeast),
            ("curva6", 48.28032, 125.2, Cardinals_Points.Northwest),
            ("recta7", 579.3638, 275.2, Cardinals_Points.Northwest),
            ("curva7", 209.2147, 85.9, Cardinals_Points.Southeast),
            ("recta8", 225.3082, 237.1, Cardinals_Points.Southeast),
            ("curva8", 193.1213, 76.4, Cardinals_Points.Northwest),
            ("recta9", 547.177, 277.1, Cardinals_Points.Northwest),
            ("curva9", 32.18688, 244.5, Cardinals_Points.East),
            ("recta10", 225.3082, 265.6, Cardinals_Points.East),
            ("curva10", 96.56064, 160.6, Cardinals_Points.Southeast),
            ("recta11", 96.56064, 180.5, Cardinals_Points.Southeast),
            ("curva11", 32.18688, 144.3, Cardinals_Points.South),
            ("recta12", 112.6541, 98.6, Cardinals_Points.South),
            ("curva12", 96.56064, 67.4, Cardinals_Points.North),
            ("recta13", 128.7475, 163.0, Cardinals_Points.North),
            ("curva13", 64.37376, 141.9, Cardinals_Points.Northwest),
            ("recta14", 209.2147, 195.5, Cardinals_Points.Northwest),
            ("curva14", 32.18688, 114.3, Cardinals_Points.Southwest),
            ("recta15", 265.5411, 263.9, Cardinals_Points.Southwest)
            ]