from enum import Enum

class Weather_Status(Enum):
    Sunny = 0
    Cloudy = 1
    Rainy = 2

class Weather:
    def __init__(self, wind, temperature, visibility, humidity, weather_status : Weather_Status = None):
        self.weather_status = weather_status
        self.wind = wind
        self.temperature = temperature
        self.visibility = visibility
        self.humidity = humidity

    def increase_temperature(self, increase_temperature):
        self.temperature += increase_temperature
    
    def decrease_temperature(self, decrease_temperature):
        self.temperature += decrease_temperature
    
    def increase_humidity(self, increase_humidity):
        self.temperature += increase_humidity
    
    def decrease_humidity(self, decrease_humidity):
        self.temperature += decrease_humidity
    
    def increase_visibility(self, increase_visibility):
        self.temperature += increase_visibility
    
    def decrease_visibility(self, decrease_visibility):
        self.temperature += decrease_visibility
    
    def increase_wind(self, increase_wind):
        self.temperature += increase_wind
    
    def decrease_wind(self, decrease_wind):
        self.temperature += decrease_wind

    def change_weather_status(self, new_weather_status : Weather_Status = None):
        if new_weather_status == 0:
            self.humidity-=1
            self.visibility+=1
            self.temperature+=1
            self.weather_status = new_weather_status
        elif new_weather_status == 1:
            if self.weather_status == 2:
                self.weather_status = new_weather_status
                self.humidity-=1
                self.visibility+=1
                self.temperature+=1
            else:
                self.visibility-=1
                self.temperature-=1
                self.weather_status = new_weather_status
        elif new_weather_status == 2:
            self.humidity+=1
            self.visibility-=1
            self.temperature-=1
            self.weather_status = new_weather_status

    def print(self):
        print("Clima: ", end="")
        if self.weather_status == 0:
            print("Soleado")
        elif self.weather_status == 1:
            print("Nublado")
        else:
            print("Lluvioso")
