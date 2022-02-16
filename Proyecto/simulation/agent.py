from math import pow, sqrt
from enum import Enum
from random import uniform, randint

from colorama import init, Fore

from simulation.rider import Rider
from simulation.bike import Bike

from simulation.weather import WeatherStatus
from simulation.bike import Tires
from simulation.track import SectionType

from compilation.ast.specials import RiderNode
from ai.ai import edit_action, call_ai, acceleration


def continuous_variable_generator():
    return uniform(0, 1)


def discrete_variable_generator():
    return randint(1, 10)


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
    def __init__(self, rider: Rider, bike: Bike, flag_configuration, flag_action, flag_acceleration, section, node: RiderNode = None):
        self.rider = rider
        self.bike = bike
        self.speed = bike.max_speed / 3
        self.acceleration = 0
        self.time_track = 0
        self.flag_configuration = flag_configuration
        self.flag_action = flag_action
        self.flag_acceleration = flag_acceleration
        self.flag_to_pits = False
        self.distance_to_nearest_forward = 0
        self.distance_to_nearest_behind = 0
        self.shot_down_forward = False
        self.shot_down_behind = False
        self.node = node
        self.time_lap = 0
        self.section = section
        self.sections = 0
        self.current_lap = 0

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

        if weather.is_front_wind(self.section[3]):
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
        elif weather.is_back_wind(self.section[3]):
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
    
    def change_section(self, section, last):
        self.section = section
        if last:
            self.sections = 0
            self.current_lap += 1
        else:
            self.sections += 1

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
        if new_weather.is_front_wind(self.section[3]):
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
        elif new_weather.is_back_wind(self.section[3]):
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

    def overcome_an_obstacle(self, race, forward_agent, behind_agent):
        action = self.select_action(race)
        self.select_acceleration(race, action)
        self.calc_final_speed()
        if not self.status_analysis(race, action, forward_agent, behind_agent):
            return False
        if action is not None and action.name.__contains__("Pits"):
            self.flag_to_pits = True
        return True

    def select_action(self, race):
        prob = continuous_variable_generator()
        if not self.flag_action or self.rider.independence > prob:
            edit_action(race, self)
            action = call_ai("action.py")
            prob = continuous_variable_generator()
            if self.rider.expertise > 1 - prob:
                action += randint(-1, 1)
                if action < 0:
                    action = 0
                if action > 35:
                    action = 35
            return AgentActions(action)
        else:
            self.node.refreshContext(self.__dict__)
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

    def select_acceleration(self, race, action):
        prob = continuous_variable_generator()
        if not self.flag_acceleration or self.rider.independence > prob:
            max_acceleration = self.calc_max_acceleration(min(self.bike.max_speed, self.section[2]))
            self.acceleration = acceleration(race, self, action, max_acceleration)
        else:
            self.node.refreshContext(self.__dict__)
            if self.node.funciones[0].idfun == "select_acceleration":
                function = self.node.funciones[0]
            else:
                function = self.node.funciones[1]
            function.eval([], self.node.nuevocontext)
            self.acceleration = self.node.nuevocontext.variables["acceleration"].value

    def calc_max_acceleration(self, max_speed):
        return (pow(max_speed / 3.6, 2) - pow(self.speed / 3.6, 2)) / (2 * self.section[1])

    def calc_final_speed(self):
        if self.acceleration != 0:
            v0 = self.speed / 3.6
            vf = sqrt(pow(v0, 2) + 2 * self.acceleration * self.section[1])
            t = (vf - v0) / self.acceleration
            self.time_lap += t
            self.time_track += t
            self.speed = vf * 3.6
        else:
            t = self.section[1] / self.speed
            self.time_lap += t
            self.time_track += t

    def status_analysis(self, race, action, forward_agent, behind_agent):
        if action is None:
            print(Fore.RED + "El piloto {} se ha quedado perplejo y no ha reaccionado. Ha sido descalificado.".
                  format(self.rider.name))
            return False
        if self.speed == 0:
            print(
                Fore.RED + "El piloto {} ha roto el acelerador y su moto se ha detenido en plena carrera. Ha sido descalificado.".
                format(self.rider.name))
            return False
        if self.section[4] == TrackType.Straight:
            if action.name.__contains__("Turn"):
                print(Fore.RED + "El piloto {} ha doblado en plena recta y se ha ido al suelo.".format(self.rider.name))
                return False
            expertise = self.rider.step_by_line / 1000
        else:
            if not action.name.__contains__("Turn"):
                print(Fore.RED + "El piloto {} ha seguido de largo y no ha doblado. Ha roto la moto en la grava.".
                      format(self.rider.name))
                return False
            expertise = self.rider.cornering / 1000
        expertise += self.rider.expertise
        prob = continuous_variable_generator()
        if forward_agent is not None and (action.name.__contains__("Attack") or
                                          self.time_track < forward_agent.time_track):
            if expertise > 1 - prob:
                prob = continuous_variable_generator()
                if prob < 1 / 6:
                    print(
                        Fore.RED + "El piloto {} ha sido atacado por el piloto {} de una forma muy agresiva. Los 2 se han ido al suelo.".
                        format(forward_agent.rider.name, self.rider.name))
                    self.shot_down_behind = True
                elif prob < 2 / 6:
                    print(
                        Fore.RED + "El piloto {} ha defendido de una forma muy agresiva contra el piloto {}. Los 2 se han ido al suelo.".
                        format(forward_agent.rider.name, self.rider.name))
                    self.shot_down = -1
                elif prob < 3 / 6:
                    print(
                        Fore.RED + "El piloto {} ha intentado adelantar de una forma muy agresiva y se ha ido al suelo.".
                        format(self.rider.name))
                elif prob < 3 / 6:
                    print(
                        Fore.RED + "El piloto {} se ha ido al suelo, atacado por el piloto {} de una forma muy agresiva.".
                        format(forward_agent.rider.name, self.rider.name))
                elif prob < 4 / 6:
                    print(
                        Fore.RED + "El piloto {} ha defendido de una forma muy agresiva contra el piloto {}. Los 2 se han ido al suelo.".
                        format(forward_agent.rider.name, self.rider.name))
                    self.shot_down_forward = True
                elif prob < 5 / 6:
                    print(
                        Fore.RED + "El piloto {} ha intentado bloquear de una forma muy agresiva y se ha ido al suelo.".
                        format(forward_agent.rider.name))
                else:
                    print(
                        Fore.RED + "El piloto {} se ha ido al suelo, bloqueado por el piloto {} de una forma muy agresiva.".
                        format(self.rider.name, forward_agent.rider.name))
                return False
            else:
                prob = continuous_variable_generator()
                t = continuous_variable_generator()
                if prob - self.rider.expertise < 1 / 3:
                    print(Fore.GREEN + "El piloto {} ha adelantado al piloto {}.".format(self.rider.name,
                                                                                         forward_agent.rider.name))
                    forward_agent.time_track = self.time_track + t
                    forward_agent.time_lap = self.time_lap + t
                    for i in range(len(race.agents)):
                        if race.agents[i] == self:
                            a = race.agents[i - 1]
                            race.agents[i - 1] = race.agents[i]
                            race.agents[i] = a
                            break
                else:
                    print(Fore.YELLOW + "El piloto {} ha defendido su posicion frente al piloto {}.".format(
                        forward_agent.rider.name,
                        self.rider.name))
                    self.time_track = forward_agent.time_track + t
                    self.time_lap = forward_agent.time_lap + t
                self.bike.probability_of_the_bike_breaking_down += 0.0001
                self.bike.probability_of_exploding_tires += 0.0001
                return True
        """
        elif behind_agent is not None and (action.name.__contains__("Defend") or 
                                           self.time_track > behind_agent.time_track):
            if expertise > 1 - prob:
                prob = continuous_variable_generator()
                if prob < 1 / 3:
                    print("El piloto {} ha defendido de una forma muy agresiva contra el piloto {}. Los 2 se han ido al suelo.".
                          format(self.rider.name, behind_agent.rider.name))
                    self.shot_down = 1
                elif prob < 2 / 3:
                    print("El piloto {} ha intentado bloquear de una forma muy agresiva y se ha ido al suelo.".
                          format(self.rider.name))
                else:
                    print("El piloto {} se ha ido al suelo, bloqueado por el piloto {} de una forma muy agresiva.".
                          format(forward_agent.rider.name, self.rider.name))
                return False
            else:
                prob = continuous_variable_generator()
                t = continuous_variable_generator()
                if prob - self.rider.expertise < 2 / 3:
                    print("El piloto {} ha defendido su posicion frente al piloto {}.".
                          format(self.rider.name, behind_agent.rider.name))
                    behind_agent.time_track = self.time_track + t
                    behind_agent.time_lap = self.time_lap + t
                else:
                    print("El piloto {} no ha podido defender su posicion frente al piloto {}.".
                          format(self.rider.name, behind_agent.rider.name))
                    self.time_track = behind_agent.time_track + t
                    self.time_lap = behind_agent.time_lap + t
                    for i in range(len(race.agents)):
                        if race.agents[i] == self:
                            a = race.agents[i + 1]
                            race.agents[i + 1] = race.agents[i]
                            race.agents[i] = a
                            break
                self.bike.probability_of_the_bike_breaking_down += 0.0001
                self.bike.probability_of_exploding_tires += 0.0001
                return True
        """
        if self.speed > self.section[2] or self.rider.probability_of_falling_off_the_bike > prob:
            print(Fore.RED + "El piloto {} ha perdido el control de su moto y se ha ido al suelo.".format(
                self.rider.name))
            return False
        if self.bike.probability_of_the_bike_breaking_down > prob:
            print(Fore.RED + "El piloto {} ha explotado el motor de su moto.".format(self.rider.name))
            return False
        if self.bike.probability_of_exploding_tires > prob:
            print(Fore.RED + "El piloto {} ha reventado los neumaticos de su moto.".format(self.rider.name))
            return False
        if self.speed > self.bike.max_speed:
            print(Fore.RED + "El piloto {} ha sobrepasado la velocidad maxima de su moto y ha explotado el motor.".
                  format(self.rider.name))
            return False
        return True

    def add_time_for_pits(self):
        self.time_lap += uniform(8, 3)

    def __lt__(self, other):
        if not isinstance(other, Agent):
            return False
        return self.time_track < other.time_track

    def __gt__(self, other):
        if not isinstance(other, Agent):
            return False
        return self.time_track > other.time_track