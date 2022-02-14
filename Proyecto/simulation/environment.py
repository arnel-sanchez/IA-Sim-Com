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
        self.weather = Weather(temperature, visibility, wind_intensity, humidity, CardinalsPoints(wind),
                               WeatherStatus(weather_status))

    def change_weather_params(self):
        if self.weather.weather_status is WeatherStatus.Rainy:
            self.weather.increase_humidity(1)
            self.weather.decrease_temperature(1)
        elif self.weather.weather_status is WeatherStatus.Sunny:
            self.weather.decrease_humidity(1)
            self.weather.increase_temperature(1)
        visibility = int(normalvariate(5, 2))
        wind_intensity = int(normalvariate(5, 2))
        self.weather.change_visibility(visibility)
        self.weather.change_wind_intensity(wind_intensity)

    def change_weather_status(self):
        wind = randint(0, 7)
        weather_status = randint(0, 2)
        self.weather.change_wind(CardinalsPoints(wind))
        self.weather.change_weather_status(weather_status)

    def print(self):
        return
