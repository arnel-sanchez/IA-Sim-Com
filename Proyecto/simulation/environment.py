from random import normalvariate, randint

from simulation.track import track_generator
from simulation.weather import Weather, CardinalsPoints, WeatherStatus

from simulation.set_off_classes.tracks.misano import Misano


class Environment:
    def __init__(self, litsAtribEnviroment):
        self.flagchangeweather=False
        track = Misano()
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
        if len(litsAtribEnviroment)>0 :
            for var in litsAtribEnviroment[0].varsforEnvironment:
                if var[0] == "track":
                    if var[2] == "shuffle":
                        track = track.shuffle()
                    elif var[2] == "random":
                        track = track_generator()
                elif var[0] == "temperature":
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
            if len(litsAtribEnviroment[0].funciones)>0:
                self.flagchangeweather=True

        self.track = track
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
        weather_status = self.weather.weather_status.value
        if weather_status == 1:
            if weather_status_random < 0.5:
                weather_status = 0
                self.weather.change_weather_status(WeatherStatus(weather_status))
                self.weather.print("El clima ha cambiado, ahora tiene una nueva configuracion")
            elif weather_status_random > 1.5:
                weather_status = 2
                self.weather.change_weather_status(WeatherStatus(weather_status))
                self.weather.print("El clima ha cambiado, ahora tiene una nueva configuracion")
        elif weather_status == 0:
            if weather_status_random < 0.5:
                weather_status = 1
                self.weather.change_weather_status(WeatherStatus(weather_status))
                self.weather.print("El clima ha cambiado, ahora tiene una nueva configuracion")
            elif weather_status_random > 1.5:
                weather_status = 2
                self.weather.change_weather_status(WeatherStatus(weather_status))
                self.weather.print("El clima ha cambiado, ahora tiene una nueva configuracion")
        else:
            if weather_status_random < 0.5:
                weather_status = 0
                self.weather.change_weather_status(WeatherStatus(weather_status))
                self.weather.print("El clima ha cambiado, ahora tiene una nueva configuracion")
            elif weather_status_random > 1.5:
                weather_status = 1
                self.weather.change_weather_status(WeatherStatus(weather_status))
                self.weather.print("El clima ha cambiado, ahora tiene una nueva configuracion")
        self.weather.change_wind(CardinalsPoints(wind))
