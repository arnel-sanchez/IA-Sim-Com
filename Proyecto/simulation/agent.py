from math import pow, sqrt
from enum import Enum
from random import normalvariate

from simulation.rider import Rider
from simulation.bike import Bike

from simulation.weather import WeatherStatus
from simulation.bike import Tires
from simulation.track import TrackType

from compilation.ast.specials import RiderNode
from ai.ai import edit_action, call_ai, acceleration


class Agent:
    def __init__(self, rider: Rider, bike: Bike, flag_configuration, flag_action, flag_acceleration, node: RiderNode = None):
        self.rider = rider
        self.bike = bike
        self.speed = 0
        self.acceleration = 0
        self.time_track = 0
        self.flag_configuration = flag_configuration
        self.flag_action = flag_action
        self.flag_acceleration = flag_acceleration
        self.flag_to_pits = False
        self.distance_to_nearest_forward = 0
        self.distance_to_nearest_behind = 0
        self.shot_down = 0
        self.node = node

    def update_agent_initial_parameters(self, weather, section):
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
            if self.bike.probability_of_exploding_tires + 0.001 * (weather.temperature - 5) / 3 >= 1:
                self.bike.probability_of_exploding_tires = 1
            else:
                self.bike.probability_of_exploding_tires += 0.001 * (weather.temperature - 5) / 3
            if self.bike.probability_of_the_bike_breaking_down + 0.001 * (weather.temperature - 5) / 3 >= 1:
                self.bike.probability_of_the_bike_breaking_down = 1
            else:
                self.bike.probability_of_the_bike_breaking_down += 0.001 * (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.001 * (weather.temperature - 5) / 3
        elif weather.temperature < 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            if self.bike.probability_of_exploding_tires - 0.001 * (weather.temperature - 5) / 3 <= 0:
                self.bike.probability_of_exploding_tires = 0
            else:
                self.bike.probability_of_exploding_tires -= 0.001 * (weather.temperature - 5) / 3
            if self.bike.probability_of_the_bike_breaking_down - 0.001 * (weather.temperature - 5) / 3 <= 0:
                self.bike.probability_of_the_bike_breaking_down = 0
            else:
                self.bike.probability_of_the_bike_breaking_down -= 0.001 * (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike + 0.001 * (weather.temperature - 5) / 2 >= 10:
                self.rider.probability_of_falling_off_the_bike = 10
            else:
                self.rider.probability_of_falling_off_the_bike += 0.001 * (weather.temperature - 5) / 3
        if weather.visibility > 5:
            if self.rider.step_by_line + (weather.temperature - 5) / 3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5) / 3
            if self.rider.cornering + (weather.temperature - 5) / 3 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.001 * (weather.temperature - 5) / 3
        elif weather.visibility < 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike + 0.001 * (weather.temperature - 5) / 2 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.001 * (weather.temperature - 5) / 3
        if weather.humidity > 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike + 0.001 * (weather.temperature - 5) / 2 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.001 * (weather.temperature - 5) / 3
        elif weather.humidity < 5:
            if self.rider.step_by_line + (weather.temperature - 5) / 3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5) / 3
            if self.rider.cornering + (weather.temperature - 5) / 3 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.001 * (weather.temperature - 5) / 3

        if weather.is_front_wind(section[3]):
            if self.rider.step_by_line - weather.wind_intensity / 4 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= weather.wind_intensity / 4

            if self.rider.cornering - weather.wind_intensity / 4 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= weather.wind_intensity / 4
            if self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_exploding_tires + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.002 * weather.wind_intensity / 4

                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.003 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Hard and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.003 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.001 * weather.wind_intensity / 4
        elif weather.is_back_wind(section[3]):
            if self.rider.step_by_line + weather.wind_intensity / 4 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += weather.wind_intensity / 4

            if self.rider.cornering + weather.wind_intensity / 4 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += weather.wind_intensity / 4

            if self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_exploding_tires + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.002 * weather.wind_intensity / 4

                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.003 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Hard and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.003 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.001 * weather.wind_intensity / 4
        else:
            if self.rider.step_by_line - weather.wind_intensity / 4 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= weather.wind_intensity / 4

            if self.rider.cornering - weather.wind_intensity / 4 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= weather.wind_intensity / 4

            if self.rider.probability_of_falling_off_the_bike + 0.001 * weather.wind_intensity / 4 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.001 * weather.wind_intensity / 4

    def update_agent_parameter(self, weather, new_weather, section):
        if new_weather.temperature > 5 and weather.temperature < 5:
            if self.rider.step_by_line + (weather.temperature - 5) / 3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5) / 3
            if self.rider.cornering + (weather.temperature - 5) / 3 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (weather.temperature - 5) / 3
            if self.bike.probability_of_exploding_tires + 0.001 * (weather.temperature - 5) / 3 >= 1:
                self.bike.probability_of_exploding_tires = 1
            else:
                self.bike.probability_of_exploding_tires += 0.001 * (weather.temperature - 5) / 3
            if self.bike.probability_of_the_bike_breaking_down + 0.001 * (weather.temperature - 5) / 3 >= 1:
                self.bike.probability_of_the_bike_breaking_down = 1
            else:
                self.bike.probability_of_the_bike_breaking_down += 0.001 * (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.001 * (weather.temperature - 5) / 3
        elif new_weather.temperature < 5 and weather.temperature > 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            if self.bike.probability_of_exploding_tires - 0.001 * (weather.temperature - 5) / 3 <= 0:
                self.bike.probability_of_exploding_tires = 0
            else:
                self.bike.probability_of_exploding_tires -= 0.001 * (weather.temperature - 5) / 3
            if self.bike.probability_of_the_bike_breaking_down - 0.001 * (weather.temperature - 5) / 3 <= 0:
                self.bike.probability_of_the_bike_breaking_down = 0
            else:
                self.bike.probability_of_the_bike_breaking_down -= 0.001 * (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike + 0.001 * (weather.temperature - 5) / 2 >= 10:
                self.rider.probability_of_falling_off_the_bike = 10
            else:
                self.rider.probability_of_falling_off_the_bike += 0.001 * (weather.temperature - 5) / 3
        if new_weather.visibility > 5 and weather.visibility < 5:
            if self.rider.step_by_line + (weather.temperature - 5) / 3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5) / 3
            if self.rider.cornering + (weather.temperature - 5) / 3 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.001 * (weather.temperature - 5) / 3
        elif new_weather.visibility < 5 and weather.visibility > 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike + 0.001 * (weather.temperature - 5) / 2 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.001 * (weather.temperature - 5) / 3
        if new_weather.humidity > 5 and weather.humidity < 5:
            if self.rider.step_by_line - (weather.temperature - 5) / 3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5) / 3
            if self.rider.cornering - (weather.temperature - 5) / 3 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike + 0.001 * (weather.temperature - 5) / 2 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.001 * (weather.temperature - 5) / 3
        elif new_weather.humidity < 5 and weather.humidity > 5:
            if self.rider.step_by_line + (weather.temperature - 5) / 3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5) / 3
            if self.rider.cornering + (weather.temperature - 5) / 3 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (weather.temperature - 5) / 3
            if self.rider.probability_of_falling_off_the_bike - 0.001 * (weather.temperature - 5) / 2 <= 0:
                self.rider.probability_of_falling_off_the_bike = 0
            else:
                self.rider.probability_of_falling_off_the_bike -= 0.001 * (weather.temperature - 5) / 3

        if new_weather.is_front_wind(section[3]):
            if self.rider.step_by_line - weather.wind_intensity / 4 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= weather.wind_intensity / 4

            if self.rider.cornering - weather.wind_intensity / 4 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= weather.wind_intensity / 4
            if self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_exploding_tires + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.002 * weather.wind_intensity / 4

                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.003 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Hard and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.003 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.001 * weather.wind_intensity / 4
        elif new_weather.is_back_wind(section[3]):
            if self.rider.step_by_line + weather.wind_intensity / 4 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += weather.wind_intensity / 4

            if self.rider.cornering + weather.wind_intensity / 4 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += weather.wind_intensity / 4

            if self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_exploding_tires + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.002 * weather.wind_intensity / 4

                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.003 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Sunny:
                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Soft and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.001 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Medium and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Slick_Hard and weather.weather_status == WeatherStatus.Rainy:
                if self.rider.probability_of_falling_off_the_bike + 0.003 * weather.wind_intensity / 4 >= 1:
                    self.rider.probability_of_falling_off_the_bike = 1
                else:
                    self.rider.probability_of_falling_off_the_bike += 0.003 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Soft and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.002 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.002 * weather.wind_intensity / 4
            elif self.bike.tires == Tires.Rain_Medium and weather.weather_status == WeatherStatus.Cloudy:
                if self.bike.probability_of_the_bike_breaking_down + 0.001 * weather.wind_intensity / 4 >= 1:
                    self.bike.probability_of_the_bike_breaking_down = 1
                else:
                    self.bike.probability_of_the_bike_breaking_down += 0.001 * weather.wind_intensity / 4
        else:
            if self.rider.step_by_line - weather.wind_intensity / 4 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= weather.wind_intensity / 4

            if self.rider.cornering - weather.wind_intensity / 4 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= weather.wind_intensity / 4

            if self.rider.probability_of_falling_off_the_bike + 0.001 * weather.wind_intensity / 4 >= 1:
                self.rider.probability_of_falling_off_the_bike = 1
            else:
                self.rider.probability_of_falling_off_the_bike += 0.001 * weather.wind_intensity / 4

    def select_action(self, section, weather):
        prob = self.continuous_variable_generator()
        if not self.flag_action or self.rider.independence > prob:
            edit_action(self.speed, self.bike.max_speed, section[2], section[4].name, self.bike.tires.name, weather)
            ans = call_ai("action.py")
            return AgentActions(ans)
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

    def select_acceleration(self, section, race, weather, action):
        prob = self.continuous_variable_generator()
        if not self.flag_acceleration or self.rider.independence > prob:
            max_acceleration = self.calc_max_acceleration(min(self.bike.max_speed, section[2]), section[1])
            self.acceleration = acceleration(max_acceleration, weather, section, self.bike, self.rider)
            if self.acceleration < 0:
                if action.name.__contains__("SpeedUp"):
                    self.acceleration = 0
            x = 0
        else:
            self.node.refreshContext(self.__dict__)
            function = None
            if self.node.funciones[0].idfun == "select_acceleration":
                function = self.node.funciones[0]
            else:
                function = self.node.funciones[1]
            function.eval([], self.node.nuevocontext)
            self.acceleration = self.node.nuevocontext.variables["acceleration"].value
            
    def status_analysis(self, section, race, action, forward_agent, behind_agent):
        prob = race.continuous_variable_generator()

        if action is None:
            print("El piloto {} se ha quedado perplejo y no ha reaccionado, ha sido descalificado".format(self.rider.name))
            return False

        if self.speed == 0:
            print("El piloto {} ha roto el acelerador y su moto se ha detenido en plena carrera, ha sido descalificado".format(self.rider.name))
            return False

        if section[4] == TrackType.Straight:
            if (action.value >= 3 and action.value <= 5) or (action.value >= 9 and action.value <= 11) or (action.value >= 15 and action.value <= 17) or (action.value >= 21 and action.value <= 23) or (action.value >= 27 and action.value <= 29) or (action.value >= 33 and action.value <= 35):
                print("El piloto {} ha doblado en plena recta y se ha ido al suelo".format(self.rider.name))
                return False
        elif section[4] == TrackType.Curve:
            if (action.value <= 3 and action.value >= 5) or (action.value <= 9 and action.value >= 11) or (action.value <= 15 and action.value >= 17) or (action.value <= 21 and action.value >= 23) or (action.value <= 27 and action.value >= 29) or (action.value <= 33 and action.value >= 35):
                print("El piloto {} ha seguido de largo y no ha doblado, ha roto la moto en la grava.".format(self.rider.name))
                return False

        if action.value >= 12 and action.value <= 23 and self.rider.aggressiveness > prob:
            print("El piloto {} ha intentado adelantar de una forma muy agresiva y se ha hido al suelo.".format(self.rider.name))
            if forward_agent is not None and forward_agent.rider.aggressiveness > prob:
                print("El piloto {} ha sido atacado por el piloto {} de una forma muy agresiva y los 2 se han ido al suelo.".format(forward_agent.rider.name, self.rider.name))
                self.shot_down = -1
            return False
        elif action.value >= 24 and action.value <= 35 and self.rider.aggressiveness > prob:
            print("El piloto {} ha intentado bloquear de una forma muy agresiva y se ha hido al suelo.".format(self.rider.name))
            if behind_agent is not None and behind_agent.rider.aggressiveness > prob:
                print("El piloto {} ha sido defendido por el piloto {} de una forma muy agresiva y los 2 se han ido al suelo.".format(behind_agent.rider.name, self.rider.name))
                self.shot_down = 1
            return False

        if self.rider.probability_of_falling_off_the_bike > prob:
            print("El piloto {} ha perdido el control de su moto y se ha ido al suelo".format(self.rider.name))
            return False

        if self.bike.probability_of_the_bike_breaking_down > prob:
            print("El piloto {} ha reventado el motor de su moto".format(self.rider.name))
            return False

        if self.bike.probability_of_exploding_tires > prob:
            print("El piloto {} ha reventado los neumaticos de su moto".format(self.rider.name))
            return False

        if section[2] < self.speed and prob < 0.001:
            print("El piloto {} ha perdido el control de su moto y se ha ido al suelo".format(self.rider.name))
            return False
        elif section[2] > self.speed and prob < 0.0001:
            print("El piloto {} ha perdido el control de su moto y se ha ido al suelo".format(self.rider.name))
            return False
        elif self.speed > self.bike.max_speed:
            print("El piloto {} ha sobrepasado la velocidad maxima de su moto y ha explotado el motor".format(self.rider.name))
            return False
        return True

    def overcome_an_obstacle(self, section, race, weather, forward_agent, behind_agent):
        action = self.select_action(section, weather)
        self.select_acceleration(section, race, weather, action)
        self.calc_final_speed(section[2])
        if not self.status_analysis(section, race, action, forward_agent, behind_agent):
            return False
        if action is not None and 6 <= action.value <= 11:
            self.flag_to_pits = True
        return True

    def calc_final_speed(self, max_speed):
        y = self.speed
        vf = pow(self.speed, 2) + 2 * max_speed * self.acceleration
        if vf >= 0:
            vf = sqrt(vf)
        else:
            vf = 0
        if self.acceleration != 0:
            t = (vf - self.speed) / self.acceleration
            self.time_track += t
            self.speed = vf
        else:
            self.time_lap = 0
        if self.speed == 0:
            x = 0

    def calc_max_acceleration(self, max_speed, length):
        return (pow(max_speed/3.6, 2) - pow(self.speed/3.6, 2))/(2*length)

    def continuous_variable_generator(self):
        return normalvariate(0.5, 0.16)

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

    Attack_SpeedUp = 12
    Attack_KeepSpeed = 13
    Attack_Brake = 14
    Attack_SpeedUp_Turn = 15
    Attack_KeepSpeed_Turn = 16
    Attack_Brake_Turn = 17
    Attack_SpeedUp_Pits = 18
    Attack_KeepSpeed_Pits = 19
    Attack_Brake_Pits = 20
    Attack_SpeedUp_Turn_Pits = 21
    Attack_KeepSpeed_Turn_Pits = 22
    Attack_Brake_Turn_Pits = 23

    Defend_SpeedUp = 24
    Defend_KeepSpeed = 25
    Defend_Brake = 26
    Defend_SpeedUp_Turn = 27
    Defend_KeepSpeed_Turn = 28
    Defend_Brake_Turn = 29
    Defend_SpeedUp_Pits = 30
    Defend_KeepSpeed_Pits = 31
    Defend_Brake_Pits = 32
    Defend_SpeedUp_Turn_Pits = 33
    Defend_KeepSpeed_Turn_Pits = 34
    Defend_Brake_Turn_Pits = 35