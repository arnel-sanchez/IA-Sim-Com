from math import pow, sqrt
from enum import Enum

from simulation.rider import Rider
from simulation.bike import Bike

from simulation.weather import CardinalsPoints, WeatherStatus
from simulation.bike import Tires
from simulation.track import TrackType

from compilation.ast.nodes import RiderNode
from ai.ai import edit_action, call_ai


class Agent:
    def __init__(self, rider: Rider, bike: Bike, flag_configuration, flag_action, flag_acceleration, node: RiderNode = None):
        self.rider = rider
        self.bike = bike
        self.speed = 0
        self.acceleration = 0
        self.time_lap = 0
        self.flag_configuration = flag_configuration
        self.flag_action = flag_action
        self.flag_acceleration = flag_acceleration
        self.flag_to_pits = False
        self.node = node

    def update_agent_initial_parameters(self, weather, section):
        if self.bike.chassis_stiffness > 5:
            if self.rider.step_by_line + (self.bike.chassis_stiffness - 5) / 2 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (self.bike.chassis_stiffness - 5) / 2
            if self.rider.cornering - (self.bike.chassis_stiffness) / 2 <= 0:
                self.rider.cornering = 0
            else:
                self.rider.cornering -= self.bike.chassis_stiffness / 2
        elif self.bike.chassis_stiffness < 5:
            if self.rider.cornering + (self.bike.chassis_stiffness - 5) / 2 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (self.bike.chassis_stiffness - 5) / 2
            if self.rider.step_by_line - (self.bike.chassis_stiffness) / 2 <= 0:
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
            if self.rider.step_by_line - (self.bike.brakes) / 2 <= 0:
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
        if not self.flag_action:
            edit_action(self.speed, self.bike.max_speed, section[2], section[4].name, self.bike.tires.name, weather)
            ans = call_ai("python ai/action.py")
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
            
    def select_acceleration(self, section, race, action):
        if not self.flag_acceleration:
            if action == AgentActions.Brake:
                self.acceleration = (-1) * self.bike.acceleration / race.discrete_variable_generator()
            else:
                self.acceleration = self.bike.acceleration / race.discrete_variable_generator()
        else:
            self.node.refreshContext(self.__dict__)
            function = None
            if self.node.funciones[0].idfun == "select_acceleration":
                function = self.node.funciones[0]
            else:
                function = self.node.funciones[1]
            function.eval([], self.node.nuevocontext)
            self.acceleration = self.node.nuevocontext.variables["acceleration"].value
            
    def status_analysis(self, section, race, action):
        prob = race.continuous_variable_generator()

        if action is None:
            print("El piloto {} se ha quedado perplejo y no ha reaccionado, ha sido descalificado".format(self.rider.name))
            return False

        if self.speed == 0:
            print("El piloto {} ha roto el acelrador y su moto se ha detenido en plena carrera, ha sido descalificado".format(self.rider.name))
            return False

        if section[4] == TrackType.Straight:
            if action.value == 3 or action.value == 4 or action.value == 5 or action.value == 9 or action.value == 10 or action.value == 11:
                print("El piloto {} ha doblado en plena recta y se ha ido al suelo".format(self.rider.name))
                return False
        elif section[4] == TrackType.Curve:
            if action.value != 3 and action.value != 4 and action.value != 5 and action.value != 9 and action.value != 10 and action.value != 11:
                print("El piloto {} ha seguido de largo y no ha doblado, a roto la moto en la grava.".format(self.rider.name))
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

    def overcome_an_obstacle(self, section, race, weather):
        action = self.select_action(section, weather)
        self.select_acceleration(section, race, action)
        self.calc_final_speed(self.speed, section[2])
        if not self.status_analysis(section, race, action):
            race.agents.remove(self)
        if action is not None and 6 <= action.value <= 11:
            self.flag_to_pits = True
        return

    def calc_final_speed(self, speed, max_speed):
        vf = pow(speed, 2) + 2 * max_speed * self.acceleration
        if vf >= 0:
            vf = sqrt(vf)
        else:
            vf = 0
        if self.acceleration != 0:
            t = (vf - self.speed)/self.acceleration
            self.time_lap += t
            self.speed = vf
        else:
            self.time_lap = 0

    def calc_max_aceleration(speed_initial, speed_final, length):
        return (pow(speed_final, 2) - pow(speed_initial, 2))/2*length

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
