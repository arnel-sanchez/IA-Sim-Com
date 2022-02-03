from simulation.rider import Rider
from simulation.bike import Bike
from enum import Enum
from math import pow
from math import sqrt
from simulation.weather import Cardinals_Points

class Agent:
    def __init__(self, rider: Rider, bike: Bike):
        self.rider = rider
        self.bike = bike
        self.speed = 0
        self.acceleration = 0
        self.time_lap = 0

    def update_agent_initial_parameters(self, weather, section):
        if self.bike.chassis_stiffness > 5:
            if self.rider.step_by_line + (self.bike.chassis_stiffness - 5)/2 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (self.bike.chassis_stiffness - 5)/2
            if self.rider.cornering - (self.bike.chassis_stiffness)/2 <= 0:
               self.rider.cornering = 0
            else:
               self.rider.cornering -= self.bike.chassis_stiffness/2
        elif self.bike.chassis_stiffness < 5:
            if self.rider.cornering + (self.bike.chassis_stiffness - 5)/2 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (self.bike.chassis_stiffness - 5)/2
            if self.rider.step_by_line - (self.bike.chassis_stiffness)/2 <= 0:
               self.rider.step_by_line = 0
            else:
               self.rider.step_by_line -= self.bike.chassis_stiffness/2

        if self.bike.brakes < 5:
            if self.rider.step_by_line + (self.bike.brakes - 5)/2 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (self.bike.brakes - 5)/2
            
            if self.rider.cornering  - self.bike.brakes/2 <= 0:
               self.rider.cornering = 0
            else:
               self.rider.cornering -= self.bike.brakes/2
        elif self.bike.brakes > 5:
            if self.rider.cornering + (self.bike.brakes - 5)/2 >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering += (self.bike.brakes - 5)/2
            
            if self.rider.step_by_line  - (self.bike.brakes)/2 <= 0:
               self.rider.step_by_line = 0
            else:
               self.rider.step_by_line -= self.bike.brakes/2

        if weather.temperature > 5:
            if self.rider.step_by_line + (weather.temperature - 5)/3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5)/3
            
            if self.rider.cornering  + (weather.temperature - 5)/3 >= 10:
               self.rider.cornering = 10
            else:
               self.rider.cornering += (weather.temperature - 5)/3

            if self.bike.probability_of_exploding_tires + 0.1*(weather.temperature - 5)/3 >= 1:
                self.bike.probability_of_exploding_tires = 1
            else:
                self.bike.probability_of_exploding_tires += 0.1*(weather.temperature - 5)/3
                    
            if self.bike.probability_of_the_motorcycle_breaking_down + 0.1*(weather.temperature - 5)/3 >= 1:
                self.bike.probability_of_the_motorcycle_breaking_down = 1
            else:
                self.bike.probability_of_the_motorcycle_breaking_down += 0.1*(weather.temperature - 5)/3

            if self.rider.probability_of_falling_off_the_motorcycle - 0.1*(weather.temperature - 5)/2 <= 0:
                self.rider.probability_of_falling_off_the_motorcycle = 0
            else:
                self.rider.probability_of_falling_off_the_motorcycle -= 0.1*(weather.temperature - 5)/3
        elif weather.temperature < 5:
            if self.rider.step_by_line - (weather.temperature - 5)/3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5)/3
            
            if self.rider.cornering  - (weather.temperature - 5)/3 <= 0:
               self.rider.cornering = 0
            else:
               self.rider.cornering -= (weather.temperature - 5)/3

            if self.bike.probability_of_exploding_tires - 0.1*(weather.temperature - 5)/3 <= 0:
                self.bike.probability_of_exploding_tires = 0
            else:
                self.bike.probability_of_exploding_tires -= 0.1*(weather.temperature - 5)/3
                    
            if self.bike.probability_of_the_motorcycle_breaking_down - 0.1*(weather.temperature - 5)/3 <= 0:
                self.bike.probability_of_the_motorcycle_breaking_down = 0
            else:
                self.bike.probability_of_the_motorcycle_breaking_down -= 0.1*(weather.temperature - 5)/3

            if self.rider.probability_of_falling_off_the_motorcycle + 0.1*(weather.temperature - 5)/2 >= 10:
                self.rider.probability_of_falling_off_the_motorcycle = 10
            else:
                self.rider.probability_of_falling_off_the_motorcycle += 0.1*(weather.temperature - 5)/3
        
        if weather.visibility > 5:
            if self.rider.step_by_line + (weather.temperature - 5)/3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5)/3
            
            if self.rider.cornering  + (weather.temperature - 5)/3 >= 10:
               self.rider.cornering = 10
            else:
               self.rider.cornering += (weather.temperature - 5)/3

            if self.rider.probability_of_falling_off_the_motorcycle - 0.1*(weather.temperature - 5)/2 <= 0:
                self.rider.probability_of_falling_off_the_motorcycle = 0
            else:
                self.rider.probability_of_falling_off_the_motorcycle -= 0.1*(weather.temperature - 5)/3
        elif weather.visibility < 5:
            if self.rider.step_by_line - (weather.temperature - 5)/3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5)/3
            
            if self.rider.cornering  - (weather.temperature - 5)/3 <= 0:
               self.rider.cornering = 0
            else:
               self.rider.cornering -= (weather.temperature - 5)/3

            if self.rider.probability_of_falling_off_the_motorcycle + 0.1*(weather.temperature - 5)/2 >= 1:
                self.rider.probability_of_falling_off_the_motorcycle = 1
            else:
                self.rider.probability_of_falling_off_the_motorcycle += 0.1*(weather.temperature - 5)/3

        if weather.humidity > 5:
            if self.rider.step_by_line - (weather.temperature - 5)/3 <= 0:
                self.rider.step_by_line = 0
            else:
                self.rider.step_by_line -= (weather.temperature - 5)/3
            
            if self.rider.cornering  - (weather.temperature - 5)/3 <= 0:
               self.rider.cornering = 0
            else:
               self.rider.cornering -= (weather.temperature - 5)/3

            if self.rider.probability_of_falling_off_the_motorcycle + 0.1*(weather.temperature - 5)/2 >= 1:
                self.rider.probability_of_falling_off_the_motorcycle = 1
            else:
                self.rider.probability_of_falling_off_the_motorcycle += 0.1*(weather.temperature - 5)/3
        elif weather.humidity < 5:
            if self.rider.step_by_line + (weather.temperature - 5)/3 >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line += (weather.temperature - 5)/3
            
            if self.rider.cornering  + (weather.temperature - 5)/3 >= 10:
               self.rider.cornering = 10
            else:
               self.rider.cornering += (weather.temperature - 5)/3

            if self.rider.probability_of_falling_off_the_motorcycle - 0.1*(weather.temperature - 5)/2 <= 0:
                self.rider.probability_of_falling_off_the_motorcycle = 0
            else:
                self.rider.probability_of_falling_off_the_motorcycle -= 0.1*(weather.temperature - 5)/3

        if weather.wind == Cardinals_Points.North:
            #De Frente
            if section[3] == Cardinals_Points.North:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4
                
                if self.bike.probability_of_exploding_tires + 0.1*weather.wind_intensity/4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.1*weather.wind_intensity/4
            #De Espaldas
            elif section[3] == Cardinals_Points.South:
                if self.rider.step_by_line + weather.wind_intensity/4 >= 10:
                    self.rider.step_by_line = 10
                else:
                    self.rider.step_by_line += weather.wind_intensity/4
                
                if self.rider.cornering + weather.wind_intensity/4 >= 10:
                    self.rider.cornering = 10
                else:
                    self.rider.cornering += weather.wind_intensity/4

                if self.bike.probability_of_the_motorcycle_breaking_down + 0.1*weather.wind_intensity/4 >= 1:
                    self.bike.probability_of_the_motorcycle_breaking_down = 1
                else:
                    self.bike.probability_of_the_motorcycle_breaking_down += 0.1*weather.wind_intensity/4
            #De Lado
            else:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.rider.probability_of_falling_off_the_motorcycle + 0.1*weather.wind_intensity/4 >= 1:
                    self.rider.probability_of_falling_off_the_motorcycle = 1
                else:
                    self.rider.probability_of_falling_off_the_motorcycle += 0.1*weather.wind_intensity/4
        elif weather.wind == Cardinals_Points.East:
            #De Frente
            if section[3] == Cardinals_Points.East:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.bike.probability_of_exploding_tires + 0.1*weather.wind_intensity/4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.1*weather.wind_intensity/4
            #De Espaldas
            elif section[3] == Cardinals_Points.West:
                if self.rider.step_by_line + weather.wind_intensity/4 >= 10:
                    self.rider.step_by_line = 10
                else:
                    self.rider.step_by_line += weather.wind_intensity/4
                
                if self.rider.cornering + weather.wind_intensity/4 >= 10:
                    self.rider.cornering = 10
                else:
                    self.rider.cornering += weather.wind_intensity/4

                if self.bike.probability_of_the_motorcycle_breaking_down + 0.1*weather.wind_intensity/4 >= 1:
                    self.bike.probability_of_the_motorcycle_breaking_down = 1
                else:
                    self.bike.probability_of_the_motorcycle_breaking_down += 0.1*weather.wind_intensity/4
            #De Lado
            else:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.rider.probability_of_falling_off_the_motorcycle + 0.1*weather.wind_intensity/4 >= 1:
                    self.rider.probability_of_falling_off_the_motorcycle = 1
                else:
                    self.rider.probability_of_falling_off_the_motorcycle += 0.1*weather.wind_intensity/4
        elif weather.wind == Cardinals_Points.South:
            #De Frente
            if section[3] == Cardinals_Points.South:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.bike.probability_of_exploding_tires + 0.1*weather.wind_intensity/4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.1*weather.wind_intensity/4
            #De Espaldas
            elif section[3] == Cardinals_Points.North:
                if self.rider.step_by_line + weather.wind_intensity/4 >= 10:
                    self.rider.step_by_line = 10
                else:
                    self.rider.step_by_line += weather.wind_intensity/4
                
                if self.rider.cornering + weather.wind_intensity/4 >= 10:
                    self.rider.cornering = 10
                else:
                    self.rider.cornering += weather.wind_intensity/4

                if self.bike.probability_of_the_motorcycle_breaking_down + 0.1*weather.wind_intensity/4 >= 1:
                    self.bike.probability_of_the_motorcycle_breaking_down = 1
                else:
                    self.bike.probability_of_the_motorcycle_breaking_down += 0.1*weather.wind_intensity/4
            #De Lado
            else:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.rider.probability_of_falling_off_the_motorcycle + 0.1*weather.wind_intensity/4 >= 1:
                    self.rider.probability_of_falling_off_the_motorcycle = 1
                else:
                    self.rider.probability_of_falling_off_the_motorcycle += 0.1*weather.wind_intensity/4
        else:
            #De Frente
            if section[3] == Cardinals_Points.West:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.bike.probability_of_exploding_tires + 0.1*weather.wind_intensity/4 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.1*weather.wind_intensity/4
            #De Espaldas
            elif section[3] == Cardinals_Points.East:
                if self.rider.step_by_line + weather.wind_intensity/4 >= 10:
                    self.rider.step_by_line = 10
                else:
                    self.rider.step_by_line += weather.wind_intensity/4
                
                if self.rider.cornering + weather.wind_intensity/4 >= 10:
                    self.rider.cornering = 10
                else:
                    self.rider.cornering += weather.wind_intensity/4

                if self.bike.probability_of_the_motorcycle_breaking_down + 0.1*weather.wind_intensity/4 >= 1:
                    self.bike.probability_of_the_motorcycle_breaking_down = 1
                else:
                    self.bike.probability_of_the_motorcycle_breaking_down += 0.1*weather.wind_intensity/4
            #De Lado
            else:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.rider.probability_of_falling_off_the_motorcycle + 0.1*weather.wind_intensity/4 >= 1:
                    self.rider.probability_of_falling_off_the_motorcycle = 1
                else:
                    self.rider.probability_of_falling_off_the_motorcycle += 0.1*weather.wind_intensity/4

    def update_agent_parameter(self, weather, new_weather, section):
        if new_weather.wind == Cardinals_Points.North:
            #De Frente
            if section[3] == Cardinals_Points.North:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4
                
                if self.bike.probability_of_exploding_tires + 0.1 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.1
            #De Espaldas
            elif section[3] == Cardinals_Points.South:
                if self.rider.step_by_line + weather.wind_intensity/4 >= 10:
                    self.rider.step_by_line = 10
                else:
                    self.rider.step_by_line += weather.wind_intensity/4
                
                if self.rider.cornering + weather.wind_intensity/4 >= 10:
                    self.rider.cornering = 10
                else:
                    self.rider.cornering += weather.wind_intensity/4

                if self.bike.probability_of_the_motorcycle_breaking_down + 0.1 >= 1:
                    self.bike.probability_of_the_motorcycle_breaking_down = 1
                else:
                    self.bike.probability_of_the_motorcycle_breaking_down += 0.1
            #De Lado
            else:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.rider.probability_of_falling_off_the_motorcycle + 0.1 >= 1:
                    self.bike.probability_of_falling_off_the_motorcycle = 1
                else:
                    self.bike.probability_of_falling_off_the_motorcycle += 0.1
        elif new_weather.wind == Cardinals_Points.East:
            #De Frente
            if section[3] == Cardinals_Points.East:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.bike.probability_of_exploding_tires + 0.1 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.1
            #De Espaldas
            elif section[3] == Cardinals_Points.West:
                if self.rider.step_by_line + weather.wind_intensity/4 >= 10:
                    self.rider.step_by_line = 10
                else:
                    self.rider.step_by_line += weather.wind_intensity/4
                
                if self.rider.cornering + weather.wind_intensity/4 >= 10:
                    self.rider.cornering = 10
                else:
                    self.rider.cornering += weather.wind_intensity/4

                if self.bike.probability_of_the_motorcycle_breaking_down + 0.1 >= 1:
                    self.bike.probability_of_the_motorcycle_breaking_down = 1
                else:
                    self.bike.probability_of_the_motorcycle_breaking_down += 0.1
            #De Lado
            else:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.rider.probability_of_falling_off_the_motorcycle + 0.1 >= 1:
                    self.bike.probability_of_falling_off_the_motorcycle = 1
                else:
                    self.bike.probability_of_falling_off_the_motorcycle += 0.1
        elif new_weather.wind == Cardinals_Points.South:
            #De Frente
            if section[3] == Cardinals_Points.South:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.bike.probability_of_exploding_tires + 0.1 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.1
            #De Espaldas
            elif section[3] == Cardinals_Points.North:
                if self.rider.step_by_line + weather.wind_intensity/4 >= 10:
                    self.rider.step_by_line = 10
                else:
                    self.rider.step_by_line += weather.wind_intensity/4
                
                if self.rider.cornering + weather.wind_intensity/4 >= 10:
                    self.rider.cornering = 10
                else:
                    self.rider.cornering += weather.wind_intensity/4

                if self.bike.probability_of_the_motorcycle_breaking_down + 0.1 >= 1:
                    self.bike.probability_of_the_motorcycle_breaking_down = 1
                else:
                    self.bike.probability_of_the_motorcycle_breaking_down += 0.1
            #De Lado
            else:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.rider.probability_of_falling_off_the_motorcycle + 0.1 >= 1:
                    self.bike.probability_of_falling_off_the_motorcycle = 1
                else:
                    self.bike.probability_of_falling_off_the_motorcycle += 0.1
        else:
            #De Frente
            if section[3] == Cardinals_Points.West:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.bike.probability_of_exploding_tires + 0.1 >= 1:
                    self.bike.probability_of_exploding_tires = 1
                else:
                    self.bike.probability_of_exploding_tires += 0.1
            #De Espaldas
            elif section[3] == Cardinals_Points.East:
                if self.rider.step_by_line + weather.wind_intensity/4 >= 10:
                    self.rider.step_by_line = 10
                else:
                    self.rider.step_by_line += weather.wind_intensity/4
                
                if self.rider.cornering + weather.wind_intensity/4 >= 10:
                    self.rider.cornering = 10
                else:
                    self.rider.cornering += weather.wind_intensity/4

                if self.bike.probability_of_the_motorcycle_breaking_down + 0.1 >= 1:
                    self.bike.probability_of_the_motorcycle_breaking_down = 1
                else:
                    self.bike.probability_of_the_motorcycle_breaking_down += 0.1
            #De Lado
            else:
                if self.rider.step_by_line - weather.wind_intensity/4 <= 0:
                    self.rider.step_by_line = 0
                else:
                    self.rider.step_by_line -= weather.wind_intensity/4
                
                if self.rider.cornering - weather.wind_intensity/4 <= 0:
                    self.rider.cornering = 0
                else:
                    self.rider.cornering -= weather.wind_intensity/4

                if self.rider.probability_of_falling_off_the_motorcycle + 0.1 >= 1:
                    self.bike.probability_of_falling_off_the_motorcycle = 1
                else:
                    self.bike.probability_of_falling_off_the_motorcycle += 0.1

    def select_action(self, section, race):
        if self.speed >= section[2]:
            self.acceleration = (-1) * self.bike.acceleration/race.discrete_variable_generator()
            return Agent_actions.Brake
        else:
            self.acceleration = self.bike.acceleration/race.discrete_variable_generator()
            return Agent_actions.Speed_up

    def status_analysis(self, section, race):
        prob = race.continuous_variable_generator()

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

    def overcome_an_obstacle(self, section, race):
        if self.select_action(section, race) == Agent_actions.Speed_up :
            vf = self.calc_final_speed(self.speed, section[2], self.acceleration)
            t = (vf - self.speed)/self.acceleration
            self.time_lap += t
            self.speed = vf
            
            if self.status_analysis(section,race):
                print("Obstaculo {} superado por el piloto {}".format(section[0],self.rider.name))
            else:
                race.agents.remove(self)

        elif self.select_action(section, race) == Agent_actions.Brake :
            vf = self.calc_final_speed(self.speed, section[2], self.acceleration)
            t = (vf - self.speed)/self.acceleration
            self.time_lap += t
            self.speed = vf
            
            if self.status_analysis(section, race):
                print("Obstaculo {} superado por el piloto {}".format(section[0],self.rider.name))
            else:
                race.agents.remove(self)
        else:
            print("Obstaculo {} superado por el piloto {}".format(section[0],self.rider.name))

        race.ranking()
        return

    def calc_final_speed(self, speed, max_speed, acceleration):
        a = pow(speed, 2) + 2 * max_speed * acceleration
        if a >= 0:
            return sqrt(a)
        else:
            return 0

class Agent_actions(Enum):
    Speed_up = 0
    Brake = 1
    Bend = 2
    Go_to_the_pits = 3
    Brake_Bend = 4
    Speed_up_Bend = 5
    Speed_up_Go_to_the_pits = 6
    Brake_Go_to_the_pits = 7
    Bend_Go_to_the_pits = 8
    Brake_Bend_Go_to_the_pits = 9
    Speed_up_Bend_Go_to_the_pits = 10