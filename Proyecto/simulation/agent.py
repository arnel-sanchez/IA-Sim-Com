from random import uniform, randint
from enum import Enum
from math import pow, sqrt
from colorama import Fore

from simulation.rider import Rider
from simulation.bike import Bike
from simulation.weather import WeatherStatus
from simulation.bike import Tires
from simulation.track import SectionType, PitSection
from compilation.ast.specials import RiderNode
from ai.ai import edit_action, call_ai, acceleration


def continuous_variable_generator():
    return uniform(0, 1)


def number_digits(number):
    return len(str(number))


def seconds_to_minutes(seconds):
    seconds = round(seconds, 10)
    minutes = int(seconds / 60)
    seconds -= minutes * 60
    seconds = round(seconds, 10)
    if seconds < 10:
        while number_digits(seconds) < 13:
            seconds = str(seconds) + "0"
        time = f"{minutes:02d}:0{seconds}"
    else:
        while number_digits(seconds) < 14:
            seconds = str(seconds) + "0"
        time = f"{minutes:02d}:{seconds}"
    return time


class AgentActions(Enum):
    SpeedUp = 0
    KeepSpeed = 1
    Brake = 2

    SpeedUp_Turn = 3
    KeepSpeed_Turn = 4
    Brake_Turn = 5

    SpeedUp_Pits = 6
    KeepSpeed_Pits = 7
    Brake_Pits = 8

    SpeedUp_Turn_Pits = 9
    KeepSpeed_Turn_Pits = 10
    Brake_Turn_Pits = 11

    SpeedUp_Attack = 12
    KeepSpeed_Attack = 13
    Brake_Attack = 14

    SpeedUp_Turn_Attack = 15
    KeepSpeed_Turn_Attack = 16
    Brake_Turn_Attack = 17

    SpeedUp_Pits_Attack = 18
    KeepSpeed_Pits_Attack = 19
    Brake_Pits_Attack = 20

    SpeedUp_Turn_Pits_Attack = 21
    KeepSpeed_Turn_Pits_Attack = 22
    Brake_Turn_Pits_Attack = 23

    SpeedUp_Defend = 24
    KeepSpeed_Defend = 25
    Brake_Defend = 26

    SpeedUp_Turn_Defend = 27
    KeepSpeed_Turn_Defend = 28
    Brake_Turn_Defend = 29

    SpeedUp_Pits_Defend = 30
    KeepSpeed_Pits_Defend = 31
    Brake_Pits_Defend = 32

    SpeedUp_Turn_Pits_Defend = 33
    KeepSpeed_Turn_Pits_Defend = 34
    Brake_Turn_Pits_Defend = 35


class Agent:
    def __init__(self, rider: Rider, bike: Bike, flag_configuration, flag_action, flag_acceleration, section,
                 node: RiderNode = None):
        self.rider = rider
        self.bike = bike
        self.speed = bike.max_speed / 3
        self.acceleration = 0
        self.time_track = 0
        self.flag_configuration = flag_configuration
        self.flag_action = flag_action
        self.flag_acceleration = flag_acceleration
        self.shot_down = None
        self.node = node
        self.time_lap = 0
        self.section = section
        self.sections = 0
        self.current_lap = 0
        self.ranking = 0
        self.on_pits = False
        self.off_road = False
        self.translate_tire = ["Slick Suave", "Slick Medio", "Slick Duro", "De Lluvia Suave", "De Lluvia Medio"]

    def update_agent_initial_parameters(self, weather):
        if self.bike.chassis_stiffness > 5:
            if self.rider.step_by_line + self.bike.chassis_stiffness - 5 / 2 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (self.bike.chassis_stiffness - 5) / 2
            if self.rider.cornering - self.bike.chassis_stiffness / 2 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= self.bike.chassis_stiffness / 2
        elif self.bike.chassis_stiffness < 5:
            if self.rider.cornering + self.bike.chassis_stiffness - 5 / 2 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (self.bike.chassis_stiffness - 5) / 2
            if self.rider.step_by_line - self.bike.chassis_stiffness / 2 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= self.bike.chassis_stiffness / 2
        if self.bike.brakes < 5:
            if self.rider.step_by_line + (self.bike.brakes - 5) / 2 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (self.bike.brakes - 5) / 2
            if self.rider.cornering - self.bike.brakes / 2 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= self.bike.brakes / 2
        elif self.bike.brakes > 5:
            if self.rider.cornering + (self.bike.brakes - 5) / 2 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (self.bike.brakes - 5) / 2
            if self.rider.step_by_line - self.bike.brakes / 2 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= self.bike.brakes / 2
        if weather.temperature > 5:
            if self.rider.step_by_line + (weather.temperature - 5) / 3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5) / 3
            if self.rider.cornering + (weather.temperature - 5) / 3 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (weather.temperature - 5) / 3
            if self.bike.probability_of_exploding_tires + 0.0001 * (weather.temperature - 5) / 3 >= 1:
                self.bike.probability_of_exploding_tires = 1
            else:
                self.bike.probability_of_exploding_tires += 0.0001 * (weather.temperature - 5) / 3
            if self.bike.probability_of_the_bike_breaking_down + 0.0001 * (weather.temperature - 5) / 3 >= 1:
                self.bike.probability_of_the_bike_breaking_down = 1
            else:
                self.bike.probability_of_the_bike_breaking_down += 0.0001 * (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.0001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.0001 * (weather.temperature - 5) / 3
        elif weather.temperature < 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            
            if self.bike.probability_of_exploding_tires - 0.0001 * (weather.temperature - 5) / 3 <= 0:
                self.bike.probability_of_exploding_tires = 0
            else:
                self.bike.probability_of_exploding_tires -= 0.0001 * (weather.temperature - 5) / 3
            
            if self.bike.probability_of_the_bike_breaking_down - 0.0001 * (weather.temperature - 5) / 3 <= 0:
                self.bike.probability_of_the_bike_breaking_down = 0
            else:
                self.bike.probability_of_the_bike_breaking_down -= 0.0001 * (weather.temperature - 5) / 3
            
            if self.rider.probability_of_falling_off_the_bike + 0.0001 * (weather.temperature - 5) / 2 >= 10:
                self.rider.probability_of_falling_off_the_bike = 10
            else:
                self.rider.probability_of_falling_off_the_bike += 0.0001 * (weather.temperature - 5) / 3
        if weather.visibility > 5:
            if self.rider.step_by_line + (weather.temperature - 5) / 3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5) / 3
            if self.rider.cornering + (weather.temperature - 5) / 3 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.0001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.0001 * (weather.temperature - 5) / 3
        elif weather.visibility < 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            
            if self.rider.probability_of_falling_off_the_bike + 0.0001 * (weather.temperature - 5) / 2 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.0001 * (weather.temperature - 5) / 3
        if weather.humidity > 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike + 0.0001 * (weather.temperature - 5) / 2 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.0001 * (weather.temperature - 5) / 3
        elif weather.humidity < 5:
            if self.rider.step_by_line + (weather.temperature - 5) / 3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5) / 3
            if self.rider.cornering + (weather.temperature - 5) / 3 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.0001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.0001 * (weather.temperature - 5) / 3

        if weather.is_front_wind(self.section.orientation):
            if self.rider.step_by_line - weather.wind_intensity / 4 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= weather.wind_intensity / 4

            if self.rider.cornering - weather.wind_intensity / 4 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= weather.wind_intensity / 4
            if self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_exploding_tires + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.0002 * weather.wind_intensity / 4

                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0003 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Hard and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0003 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0001 * weather.wind_intensity / 4
        elif weather.is_back_wind(self.section.orientation):
            if self.rider.step_by_line + weather.wind_intensity / 4 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += weather.wind_intensity / 4

            if self.rider.cornering + weather.wind_intensity / 4 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += weather.wind_intensity / 4

            if self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_exploding_tires + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.0002 * weather.wind_intensity / 4

                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0003 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Hard and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0003 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0001 * weather.wind_intensity / 4
        else:
            if self.rider.step_by_line - weather.wind_intensity / 4 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= weather.wind_intensity / 4

            if self.rider.cornering - weather.wind_intensity / 4 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= weather.wind_intensity / 4

            if self.rider.probability_of_falling_off_the_bike + 0.0001 * weather.wind_intensity / 4 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.0001 * weather.wind_intensity / 4

    def change_section(self, race):
        if self.sections == len(race.environment.track.sections) - 1:
            self.section = race.environment.track.sections[0]
            self.sections = 0
            self.current_lap += 1
            if self.on_pits:
                self.bike.select_configuration(race.environment)
                print(Fore.CYAN + "El piloto {} ha cambiado de moto ".format(self.rider.name)+"y ha montado neumaticos {}.".format(self.translate_tire[self.bike.tires.value]))
            return True
        else:
            self.sections += 1
            self.section = race.environment.track.sections[self.sections]
            return False

    def update_agent_parameter(self, weather, new_weather):
        if new_weather.temperature > 5 and weather.temperature < 5:
            if self.rider.step_by_line + (weather.temperature - 5) / 3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5) / 3
            if self.rider.cornering + (weather.temperature - 5) / 3 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (weather.temperature - 5) / 3
            if self.bike.probability_of_exploding_tires + 0.0001 * (weather.temperature - 5) / 3 >= 1:
                self.bike.probability_of_exploding_tires = 1
            else:
                self.bike.probability_of_exploding_tires += 0.0001 * (weather.temperature - 5) / 3
            if self.bike.probability_of_the_bike_breaking_down + 0.0001 * (weather.temperature - 5) / 3 >= 1:
                self.bike.probability_of_the_bike_breaking_down = 1
            else:
                self.bike.probability_of_the_bike_breaking_down += 0.0001 * (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.0001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.0001 * (weather.temperature - 5) / 3
        elif new_weather.temperature < 5 and weather.temperature > 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            if self.bike.probability_of_exploding_tires - 0.0001 * (weather.temperature - 5) / 3 <= 0:
                self.bike.probability_of_exploding_tires = 0
            else:
                self.bike.probability_of_exploding_tires -= 0.0001 * (weather.temperature - 5) / 3
            if self.bike.probability_of_the_bike_breaking_down - 0.0001 * (weather.temperature - 5) / 3 <= 0:
                self.bike.probability_of_the_bike_breaking_down = 0
            else:
                self.bike.probability_of_the_bike_breaking_down -= 0.0001 * (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike + 0.0001 * (weather.temperature - 5) / 2 >= 10:
                self.rider.probability_of_falling_off_the_bike = 10
            else:
                self.rider.probability_of_falling_off_the_bike += 0.0001 * (weather.temperature - 5) / 3
        if new_weather.visibility > 5 and weather.visibility < 5:
            if self.rider.step_by_line + (weather.temperature - 5) / 3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5) / 3
            if self.rider.cornering + (weather.temperature - 5) / 3 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.0001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.0001 * (weather.temperature - 5) / 3
        elif new_weather.visibility < 5 and weather.visibility > 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike + 0.0001 * (weather.temperature - 5) / 2 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.0001 * (weather.temperature - 5) / 3
        if new_weather.humidity > 5 and weather.humidity < 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike + 0.0001 * (weather.temperature - 5) / 2 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.0001 * (weather.temperature - 5) / 3
        elif new_weather.humidity < 5 and weather.humidity > 5:
            if self.rider.step_by_line + (weather.temperature - 5) / 3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5) / 3
            if self.rider.cornering + (weather.temperature - 5) / 3 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.0001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.0001 * (weather.temperature - 5) / 3
        if new_weather.is_front_wind(self.section.orientation):
            if self.rider.step_by_line - weather.wind_intensity / 4 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= weather.wind_intensity / 4

            if self.rider.cornering - weather.wind_intensity / 4 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= weather.wind_intensity / 4
            if self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_exploding_tires + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.0002 * weather.wind_intensity / 4

                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0003 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Hard and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0003 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0001 * weather.wind_intensity / 4
        elif new_weather.is_back_wind(self.section.orientation):
            if self.rider.step_by_line + weather.wind_intensity / 4 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += weather.wind_intensity / 4

            if self.rider.cornering + weather.wind_intensity / 4 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += weather.wind_intensity / 4

            if self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_exploding_tires + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.0002 * weather.wind_intensity / 4

                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0003 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Hard and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.0003 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.0003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.0002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.0001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.0001 * weather.wind_intensity / 4
        else:
            if self.rider.step_by_line - weather.wind_intensity / 4 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= weather.wind_intensity / 4
            if self.rider.cornering - weather.wind_intensity / 4 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= weather.wind_intensity / 4
            if self.rider.probability_of_falling_off_the_bike + 0.0001 * weather.wind_intensity / 4 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.0001 * weather.wind_intensity / 4

    def overcome_section(self, race):
        action = self.select_action(race)
        if self.section.pit_line == PitSection.Start and race.current_lap != race.laps - 1 and \
                action.name.__contains__("Pits"):
            self.on_pits = True
            print(Fore.WHITE + "El piloto {} ha entrado a boxes.".format(self.rider.name))
        if not self.overtake(race, action):
            return False
        self.select_acceleration(race, action)
        self.calc_final_speed()
        if self.sections != 0 and not self.status_analysis(action):
            self.off_road = True
            return False
        if self.on_pits and self.section.pit_line == PitSection.End:
            self.on_pits = False
            self.bike.select_configuration(race.environment)
            print(Fore.WHITE + "El piloto {} ha salido de boxes.".format(self.rider.name))
        return True

    def select_action(self, race):
        prob = continuous_variable_generator()
        if not self.flag_action or self.rider.independence > prob:
            edit_action(race, self)
            action = call_ai("action.py")
            action = AgentActions[action]
            prob = continuous_variable_generator()
            if self.rider.expertise > 1 - prob:
                value = action.value + randint(-1, 1)
                if value < 0:
                    value = 0
                if value > 35:
                    value = 35
                action = AgentActions(value)
            return action
        else:
            self.node.refreshContext(self.__dict__, self.rider.__dict__, self.section.__dict__,
                                     race.environment.weather.__dict__)
            function = None
            if self.node.funciones[0].idfun == "select_action":
                function = self.node.funciones[0]
            elif len(self.node.funciones) > 1 and self.node.funciones[1].idfun == "select_action":
                function = self.node.funciones[1]
            if function is None:
                evaluation = 11
            else:
                evaluation = function.eval([], self.node.nuevocontext)
            if evaluation > 11:
                return AgentActions(11)
            else:
                return AgentActions(evaluation)

    def overtake(self, race, action):
        if action is None or self.sections == 0:
            return True
        if self.section.type == SectionType.Straight:
            expertise = self.rider.step_by_line / 1000
        else:
            expertise = self.rider.cornering / 1000
        expertise += self.rider.expertise
        if self.ranking > 0 and action.name.__contains__("Attack"):
            forward_agent = race.agents[self.ranking - 1]
            return self.attack(race, expertise, forward_agent)
        elif self.ranking < len(race.agents) - 1 and action.name.__contains__("Defend"):
            behind_agent = race.agents[self.ranking + 1]
            return self.defend(race, expertise, behind_agent)
        return True

    def attack(self, race, expertise, forward_agent):
        prob = continuous_variable_generator()
        if not self.on_pits and expertise > 1 - prob:
            prob = continuous_variable_generator()
            if prob < 1 / 3:
                print(Fore.RED +
                      "El piloto {} ha sido atacado por el piloto {} de una forma muy agresiva. Los 2 se han ido al suelo.".
                      format(forward_agent.rider.name, self.rider.name))
                self.off_road = True
                forward_agent.off_road = True
                self.shot_down = forward_agent
                return False
            elif prob < 2 / 3:
                print(
                    Fore.RED + "El piloto {} ha intentado adelantar de una forma muy agresiva y se ha ido al suelo.".
                    format(self.rider.name))
                self.off_road = True
                return False
            else:
                print(
                    Fore.RED + "El piloto {} se ha ido al suelo, atacado por el piloto {} de una forma muy agresiva.".
                    format(forward_agent.rider.name, self.rider.name))
                forward_agent.off_road = True
                self.shot_down = forward_agent
        else:
            self.bike.probability_of_the_bike_breaking_down += 0.00001
            self.bike.probability_of_exploding_tires += 0.00001
            prob = continuous_variable_generator()
            diff = (self.time_track - forward_agent.time_track) / 2
            t = continuous_variable_generator()
            if not self.on_pits and (forward_agent.on_pits or forward_agent.off_road or
                                     prob - self.rider.expertise < 1 / 3):
                print(Fore.GREEN + "El piloto {} ha adelantado al piloto {}.".format(self.rider.name,
                                                                                     forward_agent.rider.name))
                swap(race, self, forward_agent, diff, t)
            else:
                if not self.on_pits:
                    print(Fore.YELLOW + "El piloto {} ha defendido su posicion frente al piloto {}.".
                          format(forward_agent.rider.name, self.rider.name))
                penalize(self, diff, t)
            self.review(race)
        return True

    def defend(self, race, expertise, behind_agent):
        if self.on_pits:
            return True
        prob = continuous_variable_generator()
        if expertise > 1 - prob:
            prob = continuous_variable_generator()
            if prob < 1 / 3:
                print(Fore.RED +
                      "El piloto {} ha sido bloqueado por el piloto {} de una forma muy agresiva. Los 2 se han ido al suelo.".
                      format(behind_agent.rider.name, self.rider.name))
                self.off_road = True
                behind_agent.off_road = True
                self.shot_down = behind_agent
                return False
            elif prob < 2 / 3:
                print(
                    Fore.RED + "El piloto {} ha intentado bloquear de una forma muy agresiva y se ha ido al suelo.".
                    format(self.rider.name))
                self.off_road = True
                return False
            else:
                print(
                    Fore.RED + "El piloto {} se ha ido al suelo, bloqueado por el piloto {} de una forma muy agresiva.".
                    format(behind_agent.rider.name, self.rider.name))
                behind_agent.off_road = True
                self.shot_down = behind_agent
        else:
            self.bike.probability_of_the_bike_breaking_down += 0.00001
            self.bike.probability_of_exploding_tires += 0.00001
            prob = continuous_variable_generator()
            diff = (behind_agent.time_track - self.time_track) / 2
            t = continuous_variable_generator()
            if behind_agent.on_pits or behind_agent.off_road or prob - self.rider.expertise < 2 / 3:
                if not behind_agent.on_pits and not behind_agent.off_road:
                    print(Fore.YELLOW + "El piloto {} ha defendido su posicion frente al piloto {}.".
                          format(self.rider.name, behind_agent.rider.name))
                penalize(behind_agent, diff, t)
            else:
                print(Fore.GREEN + "El piloto {} ha adelantado al piloto {}.".format(behind_agent.rider.name,
                                                                                     self.rider.name))
                swap(race, behind_agent, self, diff, t)
            behind_agent.review(race)
        return True

    def review(self, race):
        if self.section.type == SectionType.Straight:
            expertise = self.rider.step_by_line / 1000
        else:
            expertise = self.rider.cornering / 1000
        expertise += self.rider.expertise
        if self.ranking > 0:
            forward_agent = race.agents[self.ranking - 1]
            if self.section == forward_agent.section and self.time_track < forward_agent.time_track:
                return self.attack(race, expertise, forward_agent)
        if self.ranking < len(race.agents) - 1:
            behind_agent = race.agents[self.ranking + 1]
            if self.section == behind_agent.section and self.time_track > behind_agent.time_track:
                return self.defend(race, expertise, behind_agent)
        return True

    def select_acceleration(self, race, action):
        prob = continuous_variable_generator()
        if not self.flag_acceleration or self.rider.independence > prob:
            max_speed = 60 if self.on_pits else min(self.bike.max_speed, self.section.max_speed)
            max_acceleration = self.calc_max_acceleration(max_speed)
            self.acceleration = acceleration(race, self, action, max_acceleration)
        else:
            self.node.refreshContext(self.__dict__, self.rider.__dict__, self.section.__dict__,
                                     race.environment.weather.__dict__)
            if self.node.funciones[0].idfun == "select_acceleration":
                function = self.node.funciones[0]
            else:
                function = self.node.funciones[1]
            function.eval([], self.node.nuevocontext)
            self.acceleration = self.node.nuevocontext.variables["acceleration"].value

    def calc_max_acceleration(self, max_speed):
        length = self.section.pit_length if self.on_pits else self.section.length
        return (pow(max_speed / 3.6, 2) - pow(self.speed / 3.6, 2)) / (2 * length)

    def calc_final_speed(self):
        length = self.section.pit_length if self.on_pits else self.section.length
        if self.acceleration != 0:
            v0 = self.speed / 3.6
            vf = sqrt(pow(v0, 2) + 2 * self.acceleration * length)
            t = (vf - v0) / self.acceleration
            self.speed = vf * 3.6
        else:
            t = length / self.speed
        self.time_track += t
        self.time_lap += t

    def status_analysis(self, action):
        if action is None:
            print(Fore.RED + "El piloto {} se ha quedado perplejo y no ha reaccionado. Ha sido descalificado.".
                  format(self.rider.name))
            return False
        if self.speed == 0:
            print(
                Fore.RED + "El piloto {} ha roto el acelerador y su moto se ha detenido en plena carrera. Ha sido descalificado.".
                format(self.rider.name))
            return False
        if self.speed > self.bike.max_speed:
            print(Fore.RED + "El piloto {} ha sobrepasado la velocidad maxima de su moto y ha explotado el motor.".
                  format(self.rider.name))
            return False
        if self.on_pits and self.speed > 60:
            print(Fore.RED + "El piloto {} ha seguido descalificado por exceder la velocidad maxima en el Pit Line".
                  format(self.rider.name))
            return False
        if self.section.type == SectionType.Straight:
            if action.name.__contains__("Turn"):
                print(Fore.RED + "El piloto {} ha doblado en plena recta y se ha ido al suelo.".format(self.rider.name))
                return False
        else:
            if not action.name.__contains__("Turn"):
                print(Fore.RED + "El piloto {} ha seguido de largo y no ha doblado. Ha roto la moto en la grava.".
                      format(self.rider.name))
                return False
        prob = continuous_variable_generator()
        if self.speed > self.section.max_speed or prob < self.rider.probability_of_falling_off_the_bike:
            print(Fore.RED + "El piloto {} ha perdido el control de su moto y se ha ido al suelo.".
                  format(self.rider.name))
            return False
        if prob < self.bike.probability_of_the_bike_breaking_down:
            print(Fore.RED + "El piloto {} ha explotado el motor de su moto.".format(self.rider.name))
            return False
        if prob < self.bike.probability_of_exploding_tires:
            print(Fore.RED + "El piloto {} ha reventado los neumaticos de su moto.".format(self.rider.name))
            return False
        return True

    def __lt__(self, other):
        if not isinstance(other, Agent):
            return False
        return self.time_track < other.time_track

    def __gt__(self, other):
        if not isinstance(other, Agent):
            return False
        return self.time_track > other.time_track

    def print(self):
        ranking = self.ranking
        res = ""
        if 8 - number_digits(ranking) > 0:
            for j in range(8 - number_digits(ranking)):
                res += " "
        res += Fore.BLUE + "{}".format(ranking + 1) + Fore.WHITE + " -" + Fore.CYAN + " {}".format(
            seconds_to_minutes(self.time_track)) + Fore.WHITE + " -" + Fore.GREEN + " {}".format(
            seconds_to_minutes(self.time_lap)) + Fore.WHITE + " -" + Fore.RED + " {} con la {}".format(
            self.rider.name, self.bike.brand + " " + self.bike.model) + "\n"
        self.time_lap = 0
        return res

    def print_end(self):
        ranking = self.ranking
        res = ""
        if 8 - number_digits(ranking) > 0:
            for j in range(8 - number_digits(ranking)):
                res += " "
        res += Fore.BLUE + "{}".format(ranking + 1) + Fore.WHITE + " -" + Fore.CYAN + " {}".format(
            seconds_to_minutes(self.time_track)) + Fore.WHITE + " -" + Fore.RED + " {} con la {}".format(
            self.rider.name, self.bike.brand + " " + self.bike.model) + "\n"
        self.time_lap = 0
        return res


def swap(race, agent_1: Agent, agent_2, diff, t):
    if diff > 0:
        agent_2.time_track += diff + t
        agent_2.time_lap += diff + t
    agent_1.ranking -= 1
    race.agents[agent_1.ranking] = agent_1
    agent_2.ranking += 1
    race.agents[agent_2.ranking] = agent_2
    agent_2.review(race)


def penalize(agent: Agent, diff, t):
    if diff > 0:
        return
    diff *= (-1)
    agent.time_track += diff + t
    agent.time_lap += diff + t
