from random import normalvariate, randint

from simulation.track import Track
from simulation.weather import Weather, CardinalsPoints, WeatherStatus


class Environment:
    def __init__(self, track: Track):
        self.track = track
        temperature = int(normalvariate(5, 2))
        visibility = int(normalvariate(5, 2))
        humidity = int(normalvariate(5, 2))
        wind_intensity = int(normalvariate(5, 2))
        wind = randint(0, 7)
        weather_status = randint(0, 2)
        self.weather = Weather(temperature, visibility, wind_intensity, humidity, CardinalsPoints(wind), WeatherStatus(weather_status))

    def change_weather(self):
        return

    def print(self):
        return
