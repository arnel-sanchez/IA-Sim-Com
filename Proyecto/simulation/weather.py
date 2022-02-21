from enum import Enum
from colorama import Fore


class WeatherStatus(Enum):
    Sunny = 0
    Cloudy = 1
    Rainy = 2


class CardinalsPoints(Enum):
    North = 0
    Northeast = 1
    East = 2
    Southeast = 3
    South = 4
    Southwest = 5
    West = 6
    Northwest = 7


def opposite_direction(direction_1, direction_2):
    if direction_1 == CardinalsPoints.South and direction_2.name.__contains__("North"):
        return True
    elif direction_1 == CardinalsPoints.Northeast and direction_2 in [CardinalsPoints.South, CardinalsPoints.Southwest,
                                                                      CardinalsPoints.West]:
        return True
    elif direction_1 == CardinalsPoints.West and direction_2.name.__contains__("East"):
        return True
    elif direction_1 == CardinalsPoints.Southeast and direction_2 in [CardinalsPoints.North, CardinalsPoints.Northwest,
                                                                      CardinalsPoints.West]:
        return True
    elif direction_1 == CardinalsPoints.North and direction_2.name.__contains__("South"):
        return True
    elif direction_1 == CardinalsPoints.Southwest and direction_2 in [CardinalsPoints.North, CardinalsPoints.Northeast,
                                                                      CardinalsPoints.East]:
        return True
    elif direction_1 == CardinalsPoints.East and direction_2.name.__contains__("West"):
        return True
    elif direction_1 == CardinalsPoints.Northwest and direction_2 in [CardinalsPoints.South, CardinalsPoints.Southeast,
                                                                      CardinalsPoints.East]:
        return True
    return False


def measure(number):
    return "Alta" if number > 6 else "Baja" if number < 4 else "Media"


class Weather:
    def __init__(self, temperature, visibility, wind_intensity, humidity, wind: CardinalsPoints,
                 weather_status: WeatherStatus):
        self.weather_status = weather_status
        self.wind = wind
        self.temperature = temperature
        self.visibility = visibility
        self.humidity = humidity
        self.wind_intensity = wind_intensity
        self.translate_weather = ["Soleado", "Nublado", "Lluvioso"]
        self.translate_direction = ["Norte", "Noreste", "Este", "Sureste", "Sur", "Suroeste", "Oeste", "Noroeste"]

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
            self.visibility -= decrease_visibility

    def increase_wind_intensity(self, increase_wind):
        if self.wind_intensity + increase_wind >= 10:
            self.wind_intensity = 10
        else:
            self.wind_intensity += increase_wind

    def decrease_wind_intensity(self, decrease_wind):
        if self.wind_intensity - decrease_wind <= 0:
            self.wind_intensity = 0
        else:
            self.wind_intensity -= decrease_wind

    def change_temperature(self, temperature):
        self.temperature = temperature

    def change_humidity(self, humidity):
        self.humidity = humidity

    def change_visibility(self, visibility):
        self.visibility = visibility

    def change_wind_intensity(self, wind_intensity):
        self.wind_intensity = wind_intensity

    def change_weather_status(self, new_weather_status: WeatherStatus):
        if new_weather_status.value == 0:
            self.decrease_humidity(2)
            self.increase_visibility(2)
            self.increase_temperature(2)
            self.weather_status = WeatherStatus(new_weather_status)
        elif new_weather_status.value == 1:
            if self.weather_status.value == 2:
                self.weather_status = WeatherStatus(new_weather_status)
                self.decrease_humidity(2)
                self.increase_visibility(2)
                self.increase_temperature(2)
            else:
                self.decrease_visibility(2)
                self.decrease_temperature(2)
                self.weather_status = WeatherStatus(new_weather_status)
        elif new_weather_status.value == 2:
            self.increase_humidity(2)
            self.decrease_visibility(2)
            self.decrease_temperature(2)
            self.weather_status = WeatherStatus(new_weather_status)

    def change_wind(self, new_wind: CardinalsPoints):
        self.wind = CardinalsPoints(new_wind)

    def is_front_wind(self, other_wind: CardinalsPoints):
        return opposite_direction(self.wind, other_wind)

    def is_back_wind(self, wind: CardinalsPoints):
        return self.wind == wind

    def print(self, log):
        print(Fore.MAGENTA + "\n"+log+":")
        print(Fore.CYAN + "Estado: {}".format(self.translate_weather[self.weather_status.value]))
        print(Fore.CYAN + "Humedad: {}".format(measure(self.humidity)))
        print(Fore.CYAN + "Temperatura: {}".format(measure(self.temperature)))
        print(Fore.CYAN + "Visibilidad: {}".format(measure(self.visibility)))
        print(Fore.CYAN + "Viento: {}, Intensidad {}\n".format(self.translate_direction[self.wind.value],
                                                               measure(self.wind_intensity)))
