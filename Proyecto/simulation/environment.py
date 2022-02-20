from random import normalvariate, randint

from simulation.track import Track
from simulation.weather import Weather, CardinalsPoints, WeatherStatus


class Environment:
    def __init__(self, track: Track, litsAtribEnviroment):
        self.track = track
        temperature = int(normalvariate(5, 2))
        visibility = int(normalvariate(5, 2))
        humidity = int(normalvariate(5, 2))
        wind_intensity = int(normalvariate(5, 2))
        wind = randint(0, 7)
        weather_status_random = normalvariate(1, 0.4)
        if weather_status_random < 0.5:
            weather_status = 0
        elif weather_status_random > 1.5:
            weather_status = 2
        else:
            weather_status = 1
        if litsAtribEnviroment is not None:
            for var in litsAtribEnviroment:
                if var[0] == "temperature":
                    temperature = var[2]
                elif var[0] == "visibility":
                    visibility = var[2]
                elif var[0] == "wind_intensity":
                    wind_intensity = var[2]
                elif var[0] == "humidity":
                    humidity = var[2]
                elif var[0] == "wind":
                    wind = var[2]
                elif var[0] == "weather_status":
                    weather_status = var[2]
        self.weather = Weather(temperature, visibility, wind_intensity, humidity, CardinalsPoints(wind),
                               WeatherStatus(weather_status))

    def change_weather_params(self):
        if self.weather.weather_status is WeatherStatus.Rainy:
            self.weather.increase_humidity(0.5)
            self.weather.decrease_temperature(0.5)
        elif self.weather.weather_status is WeatherStatus.Sunny:
            self.weather.decrease_humidity(0.5)
            self.weather.increase_temperature(0.5)
        visibility = int(normalvariate(5, 2))
        wind_intensity = int(normalvariate(5, 2))
        self.weather.change_visibility(visibility)
        self.weather.change_wind_intensity(wind_intensity)

    def change_weather_status(self):
        wind = randint(0, 7)
        weather_status_random = normalvariate(1, 0.4)
        weather_status = 1
        if weather_status_random < 0.5:
            weather_status = 0
        elif weather_status_random > 1.5:
            weather_status = 2
        self.weather.change_wind(CardinalsPoints(wind))
        self.weather.change_weather_status(WeatherStatus(weather_status))
