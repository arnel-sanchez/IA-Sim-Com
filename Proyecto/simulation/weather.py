from enum import Enum


class WeatherStatus(Enum):
    Sunny = 0
    Cloudy = 1
    Rainy = 2


class CardinalsPoints(Enum):
    North = 0
    East = 1
    West = 2
    South = 3
    Northwest = 4
    Southwest = 5
    Southeast = 6
    Northeast = 7


class Weather:
    def __init__(self, temperature, visibility, wind_intensity, humidity, wind: CardinalsPoints, weather_status: WeatherStatus):
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

    def change_temperature(self, temperature):
        self.temperature = temperature
    
    def change_humidity(self, humidity):
        self.humidity = humidity
    
    def change_visibility(self, visibility):
        self.visibility = visibility
    
    def change_wind_intensity(self, wind_intensity):
        self.wind_intensity = wind_intensity

    def change_weather_status(self, new_weather_status: WeatherStatus):
        if new_weather_status == 0:
            self.decrease_humidity(2)
            self.increase_visibility(2)
            self.increase_temperature(2)
            self.weather_status = WeatherStatus(new_weather_status)
        elif new_weather_status == 1:
            if self.weather_status == 2:
                self.weather_status = WeatherStatus(new_weather_status)
                self.decrease_humidity(2)
                self.increase_visibility(2)
                self.increase_temperature(2)
            else:
                self.decrease_visibility(2)
                self.decrease_temperature(2)
                self.weather_status = WeatherStatus(new_weather_status)
        elif new_weather_status == 2:
            self.increase_humidity(2)
            self.decrease_visibility(2)
            self.decrease_temperature(2)
            self.weather_status = WeatherStatus(new_weather_status)

    def change_wind(self, new_wind: CardinalsPoints):
        self.wind = CardinalsPoints(new_wind)

    def print(self):
        print("Clima: ", end="")
        if self.weather_status == 0:
            print("Soleado")
        elif self.weather_status == 1:
            print("Nublado")
        else:
            print("Lluvioso")

    def is_front_wind(self, wind: CardinalsPoints):
        if self.wind == CardinalsPoints.North and wind == CardinalsPoints.South:
            return True
        elif self.wind == CardinalsPoints.South and wind == CardinalsPoints.North:
            return True
        elif self.wind == CardinalsPoints.East and wind == CardinalsPoints.West:
            return True
        elif self.wind == CardinalsPoints.West and wind == CardinalsPoints.East:
            return True
        elif self.wind == CardinalsPoints.Northeast and wind == CardinalsPoints.Southwest:
            return True
        elif self.wind == CardinalsPoints.Southwest and wind == CardinalsPoints.Northeast:
            return True
        elif self.wind == CardinalsPoints.Northwest and wind == CardinalsPoints.Southeast:
            return True
        elif self.wind == CardinalsPoints.Southeast and wind == CardinalsPoints.Northwest:
            return True

    def is_back_wind(self, wind: CardinalsPoints):
        if self.wind == wind:
            return True
