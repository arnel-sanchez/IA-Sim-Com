from random import normalvariate, randint

from simulation.track import track_generator
from simulation.weather import Weather, CardinalsPoints, WeatherStatus

from simulation.set_off_classes.tracks.misano import Misano


class Environment:
    def __init__(self, litsAtribEnviroment):
        self.flag_change_weather=False
        self.environments=litsAtribEnviroment
        self.i=0
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
                self.flag_change_weather=True
            

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
        if len(self.environments)>self.i+1:
            
            self.i+=1
            if len(self.environments[self.i].funciones==0):
                self.flag_change_weather=False

            self.environments[self.i].refreshContext(self.weather.__dict__)
            self.environments[self.i].eval(self.environments[self.i].nuevocontext)
            for var in self.environments[self.i].nuevocontext.variables:
                if var.id=="humidity":
                 if var.value<=10:     
                  self.weather.humidity=var.value
                 else:
                     self.weather.humidity=10
                if var.id=="visibility":
                 if var.value<=10:   
                  self.weather.visibility=var.value
                 else:
                      self.weather.visibility=10
                if var.id=="wind":
                 if var.value<=10:
                    self.weather.wind=var.value
                 else:
                     self.weather.wind=10
                if var.id=="wind_intensity":
                  if var.value<=10:
                   self.weather.wind_intensity=var.value
                  else:
                     self.weather.wind_intensity=10
                if var.id=="temperature":
                    if var.value<=10:
                     self.weather.temperature=var.value
                    else:
                     self.weather.temperature=10  
                if var.id=="weather_status":
                  if var.value<=10:
                   self.weather.weather_status=var.value
                  else:
                     self.weather.weather_status=10  

            
        else:
            self.flag_change_weather=False
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
