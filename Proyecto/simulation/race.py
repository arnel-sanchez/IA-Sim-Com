from colorama import Fore
from sys import path

from simulation.environment import Environment


def number_digits(number):
    return len(str(number))


def seconds_to_minutes(seconds):
    seconds = round(seconds, 11)
    minutes = int(seconds / 60)
    seconds -= minutes * 60
    seconds = round(seconds, 11)
    if number_digits(seconds) < 12:
        while number_digits(seconds) < 14:
            seconds = str(seconds) + "0"
        time = f"{minutes:02d}:0{seconds}"
    else:
        while number_digits(seconds) < 15:
            seconds = str(seconds) + "0"
        time = f"{minutes:02d}:{seconds}"
    return time


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
        self.flag_laps = False
        self.current_lap += 1
        if self.current_lap == self.laps:
            print(Fore.BLUE + "\nCarrera terminada")
            return True
        elif self.current_lap == self.laps - 1:
            weather = self.environment.weather
            self.environment.change_weather_status()
            for agent in self.agents:
                if agent.flag_to_pits:
                    agent.add_time_for_pits()
                    agent.bike.select_configuration(self.environment)
                agent.update_agent_parameter(weather, self.environment.weather)
            print(Fore.BLUE + "\nUltima vuelta")
            return False
        else:
            weather = self.environment.weather
            self.environment.change_weather_status()
            for agent in self.agents:
                if agent.flag_to_pits:
                    agent.add_time_for_pits()
                    agent.bike.select_configuration(self.environment)
                agent.update_agent_parameter(weather, self.environment.weather)
            return False

    def end_lap(self):
        if not self.flag_laps:
            return False
        lap = self.agents[0].current_lap
        for x in self.agents:
            if x.current_lap != lap:
                return False
        return True

    def clear(self):
        with open(path[0] + "/output.log", "w") as f:
            f.truncate(0)

    def printer(self, res):
        with open(path[0] + "/output.log", "a") as f:
            f.write(res)

    def print_ranking(self, ended):
        res = ""
        if ended:
            res += Fore.MAGENTA + "\nResultado final:"
            i = 1
            for agent in self.agents:
                spaces = ""
                if 8 - number_digits(i) > 0:
                    for j in range(8 - number_digits(i)):
                        spaces += " "
                res += spaces + Fore.BLUE + "{}".format(i) + Fore.WHITE + " -" + Fore.CYAN + " {}".format(
                    seconds_to_minutes(agent.time_track)) + Fore.WHITE + " -" + Fore.GREEN + " {}:".format(
                    seconds_to_minutes(agent.time_lap)) + Fore.RED + " {} con la {}".format(
                    agent.rider.name, agent.bike.brand + " " + agent.bike.model) + "\n"
                i += 1
                agent.time_lap = 0
        else:
            res += Fore.MAGENTA + "\nResultados de la vuelta" + Fore.CYAN + " {}:".format(self.current_lap + 1) + "\n"
        res += Fore.BLUE + "Posicion" + Fore.WHITE + " -" + Fore.CYAN + " Tiempo de Carrera" + Fore.WHITE + " -" + \
            Fore.GREEN + "  Tiempo de Vuelta:" + Fore.RED + " Piloto"
        return res

    def print_agent(self, agent):
        ranking = agent.ranking
        res = ""
        if 8 - number_digits(ranking) > 0:
            for j in range(8 - number_digits(ranking)):
                res += " "
        res += Fore.BLUE + "{}".format(ranking + 1) + Fore.WHITE + " -" + Fore.CYAN + " {}".format(
            seconds_to_minutes(agent.time_track)) + Fore.WHITE + " -" + Fore.GREEN + " {}:".format(
            seconds_to_minutes(agent.time_lap)) + Fore.RED + " {} con la {}".format(
            agent.rider.name, agent.bike.brand + " " + agent.bike.model) + "\n"
        agent.time_lap = 0
        return res
