from simulation.track import Track
from simulation.weather import Weather, Weather_Status, Cardinals_Points
import numpy as np
from math import sqrt
import random


class Environment:
    def __init__(self, track: Track):
        self.track = track

        temperature = int(random.normalvariate(5, 2))
        visibility =int(random.normalvariate(5, 2))
        humidity = int(random.normalvariate(5, 2))
        wind_intensity = int(random.normalvariate(5, 2))
        wind = random.randint(0,7)
        weather_status = random.randint(0,2)
        self.weather = Weather(temperature, visibility, wind_intensity, humidity, Cardinals_Points(wind), Weather_Status(weather_status))

    def change_weather(self):
        return

    def print(self):
        return