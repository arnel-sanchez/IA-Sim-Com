from time import sleep
from math import pow
from math import sqrt
from random import random
from random import randint
from simulation.race import Race
from simulation.agent import Agent_actions

class Simulator:
    def start(self, time: int, stop: bool, race: Race):
        print("\nPrimero se configura todo mediante DSL\n")

        print("\nInicio de la carrera\n")

        while True:
            for section in race.environment.track.sections:
                for agent in race.agents:
                    self.overcome_an_obstacle(section, agent, race)
            if race.change_lap() or len(race.agents) == 0:
                break
            sleep(time)

    def overcome_an_obstacle(self, section, agent, race):
        if self.select_action(section, agent, race.environment) == Agent_actions.Speed_up :
            vf = self.calc_final_speed(agent.speed, section[2], agent.acceleration)
            t = (vf - agent.speed)/agent.acceleration
            agent.time_lap += t
            agent.speed = vf
            
            if self.status_analysis(agent,section):
                print("Obstaculo {} superado por el piloto {}".format(section[0],agent.rider.name))
            else:
                race.agents.remove(agent)

        elif self.select_action(section, agent, race) == Agent_actions.Brake :
            vf = self.calc_final_speed(agent.speed, section[2], agent.acceleration)
            t = (vf - agent.speed)/agent.acceleration
            agent.time_lap += t
            agent.speed = vf
            
            if self.status_analysis(agent,section):
                print("Obstaculo {} superado por el piloto {}".format(section[0],agent.rider.name))
            else:
                race.agents.remove(agent)
        else:
            print("Obstaculo {} superado por el piloto {}".format(section[0],agent.rider.name))

        race.ranking()
        return

    def continuous_variable_generator(self):
        return random()

    def discrete_variable_generator(self):
        return randint(1, 11)

    def calc_final_speed(self, speed, max_speed, acceleration):
        return sqrt(pow(speed, 2) + 2 * max_speed * acceleration)

    def select_action(self, section, agent, environment):
        if agent.speed >= section[2]:
            agent.acceleration = (-1) * agent.bike.acceleration/self.discrete_variable_generator()
            return Agent_actions.Brake
        else:
            agent.acceleration = agent.bike.acceleration/self.discrete_variable_generator()
            return Agent_actions.Speed_up

    def status_analysis(self, agent, section):
        prob = self.continuous_variable_generator()

        if section[2] < agent.speed and prob < 0.001:
            print("El piloto {} ha perdido el control de su moto y se ha ido al suelo".format(agent.rider.name))
            return False
        elif section[2] > agent.speed and prob < 0.0001:
            print("El piloto {} ha perdido el control de su moto y se ha ido al suelo".format(agent.rider.name))
            return False
        elif agent.speed > agent.bike.max_speed:
            print("El piloto {} ha sobrepasado la velocidad máxima de su mot0 y ha explotado el motor".format(agent.rider.name))
            return False
        return True