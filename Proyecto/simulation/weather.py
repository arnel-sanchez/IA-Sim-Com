from enum import Enum
import enum

class Weather_Status(Enum):
    Sunny = 0
    Cloudy = 1
    Rainy = 2

class Cardinals_Points(Enum):
    North = 0
    East = 1
    West = 2
    South = 3
    Northwest = 4
    Southwest = 5
    Southeast = 6
    Northeast = 7

class Weather:
    def __init__(self, temperature, visibility, wind_intensity, humidity, wind: Cardinals_Points, weather_status: Weather_Status):
        self.weather_status = weather_status
        self.wind = wind
        self.temperature = temperature
        self.visibility = visibility
        self.humidity = humidity
        self.wind_intensity = wind_intensity

    def increase_temperature(self, increase_temperature):
        if self.temperature + increase_temperature >= 10:
            self.temperature = 10
        else:
            self.temperature += increase_temperature
    
    def decrease_temperature(self, decrease_temperature):
        if self.temperature - decrease_temperature <= 0:
            self.temperature = 0
        else:
            self.temperature -= decrease_temperature
    
    def increase_humidity(self, increase_humidity):
        if self.humidity + increase_humidity >= 10:
            self.humidity = 10
        else:
            self.humidity += increase_humidity
    
    def decrease_humidity(self, decrease_humidity):
        if self.humidity - decrease_humidity <= 0:
            self.humidity = 0
        else:
            self.humidity -= decrease_humidity
    
    def increase_visibility(self, increase_visibility):
        if self.visibility + increase_visibility >= 10:
            self.visibility = 10
        else:
            self.visibility += increase_visibility
    
    def decrease_visibility(self, decrease_visibility):
        if self.visibility - decrease_visibility <= 0:
            self.visibility = 0
        else:
            self.visibility += decrease_visibility
    
    def increase_wind_intensity(self, increase_wind):
        if self.wind_intensity + increase_wind >= 10:
            self.wind_intensity = 10
        else:
            self.wind_intensity += increase_wind
    
    def decrease_wind_intensity(self, decrease_wind):
        if self.wind_intensity - decrease_wind <= 0:
            self.wind_intensity = 0
        else:
            self.wind_intensity += decrease_wind

    def change_weather_status(self, new_weather_status : Weather_Status):
        if new_weather_status == 0:
            self.decrease_humidity(2)
            self.increase_visibility(2)
            self.increase_temperature(2)
            self.weather_status = new_weather_status
        elif new_weather_status == 1:
            if self.weather_status == 2:
                self.weather_status = new_weather_status
                self.decrease_humidity(2)
                self.increase_visibility(2)
                self.increase_temperature(2)
            else:
                self.decrease_visibility(2)
                self.decrease_temperature(2)
                self.weather_status = new_weather_status
        elif new_weather_status == 2:
            self.increase_humidity(2)
            self.decrease_visibility(2)
            self.decrease_temperature(2)
            self.weather_status = new_weather_status

    def change_wind(self, new_wind : Cardinals_Points):
        self.wind = new_wind

    def print(self):
        print("Clima: ", end="")
        if self.weather_status == 0:
            print("Soleado")
        elif self.weather_status == 1:
            print("Nublado")
        else:
            print("Lluvioso")