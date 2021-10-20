from enum import Enum

from track import Track, default_tracks
from pilot import default_pilots


class Weather(Enum):
    Sunny = 0
    Cloudy = 1
    Rainy = 2
    Windy = 3
    Foggy = 4
    Snowy = 5

    def print_weather(self):
        print("Clima: ", end="")
        if self.value == 0:
            print("Soleado")
        elif self.value == 1:
            print("Nublado")
        elif self.value == 2:
            print("Lluvioso")
        elif self.value == 3:
            print("Ventoso")
        elif self.value == 4:
            print("Neblinoso")
        else:
            print("Nevado")


class Race:
    def __init__(self, track: Track, pilots: list, weather: Weather = Weather.Sunny, laps: int = 20):
        self.track = track
        self.pilots = pilots
        self.weather = weather
        self.laps = laps


def race():
    tracks = default_tracks()
    misano = tracks["misano"]

    pilots = default_pilots()

    weather = Weather.Sunny

    return Race(misano, pilots, weather)
