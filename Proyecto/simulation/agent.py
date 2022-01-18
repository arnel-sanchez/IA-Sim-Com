from simulation.rider import Rider
from simulation.bike import Bike
from enum import Enum
from math import pow
from math import sqrt

class Agent:
    def __init__(self, rider: Rider, bike: Bike):
        self.rider = rider
        self.bike = bike
        self.speed = 0
        self.acceleration = 0
        self.time_lap = 0
        self.update_agent()

    def update_agent(self):
        if self.bike.chassis_stiffness >= 5:
            a = (self.rider.step_by_line + self.bike.chassis_stiffness - 5)/2
            if a >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line = a
            a = (self.rider.cornering + self.bike.chassis_stiffness - 5)/2
            if a <= 0:
               self.rider.cornering = 0
            else:
               self.rider.cornering = a
        else:
            a = (self.rider.cornering - self.bike.chassis_stiffness)/2
            if a >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering = a
            a = (self.rider.step_by_line - self.bike.chassis_stiffness)/2
            if a <= 0:
               self.rider.step_by_line = 0
            else:
               self.rider.step_by_line = a

        if self.bike.brakes < 5:
            a = (self.rider.step_by_line + self.bike.brakes - 5)/2
            if a >= 10:
                self.rider.step_by_line = 10
            else:
                self.rider.step_by_line = a
            
            a = (self.rider.cornering  + self.bike.brakes - 5)/2
            if a <= 0:
               self.rider.cornering = 0
            else:
               self.rider.cornering = a
        else:
            a = (self.rider.cornering - self.bike.brakes)/2
            if a >= 10:
                self.rider.cornering = 10
            else:
                self.rider.cornering = a
            
                a = (self.rider.step_by_line  - self.bike.brakes)/2
            if a <= 0:
               self.rider.step_by_line = 0
            else:
               self.rider.step_by_line = a

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