from sys import path
from colorama import Fore

from simulation.environment import Environment


def clear():
    with open(path[0] + "/output.log", "w") as f:
        f.truncate(0)


def printer(res):
    with open(path[0] + "/output.log", "a") as f:
        f.write(res)


class Race:
    def __init__(self, environment: Environment, agents, laps):
        self.environment = environment
        self.agents = agents
        self.laps = laps
        self.current_lap = 0
        self.ranking = agents
        self.flag_laps = False
        for agent in agents:
            agent.update_agent_initial_parameters(self.environment.weather)
            agent.bike.select_configuration(environment)

    def change_lap(self):
        self.current_lap += 1
        if self.current_lap == self.laps and self.end_lap():
            return True
        self.flag_laps = False
        old_weather = self.environment.weather
        self.environment.change_weather_params()
        new_weather = self.environment.weather
        for agent in self.agents:
            agent.update_agent_parameter(old_weather, new_weather)
        if self.current_lap == self.laps - 1:
            print(Fore.BLUE + "\nUltima vuelta")
        else:
            print(Fore.BLUE + "\nVuelta {}".format(self.current_lap + 1))
        return False

    def end_lap(self):
        if not self.flag_laps:
            return False
        lap = self.agents[0].current_lap
        for a in self.agents:
            if a.current_lap != lap:
                return False
        return True

    def print(self):
        return Fore.MAGENTA + "\nResultados de la vuelta" + Fore.CYAN + " {}:\n".format(self.current_lap + 1) + \
            Fore.BLUE + "Posicion" + Fore.WHITE + " -" + Fore.CYAN + " Tiempo de Carrera" + Fore.WHITE + \
            " -" + Fore.GREEN + " Tiempo de Vuelta" + Fore.WHITE + "  -" + Fore.RED + " Piloto\n"

    def print_end(self):
        res = Fore.MAGENTA + "\nResultado final:\n"
        res += Fore.BLUE + "Posicion" + Fore.WHITE + " -" + Fore.CYAN + " Tiempo de Carrera" + Fore.WHITE + \
            " -" + Fore.RED + " Piloto\n"
        for agent in self.agents:
            res += agent.print_end()
        return res
