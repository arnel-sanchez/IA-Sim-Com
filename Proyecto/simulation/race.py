from colorama import Fore
from sys import path

from simulation.environment import Environment


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
            print(Fore.BLUE + "\nCarrera terminada\n")
            return True
        self.flag_laps = False
        weather = self.environment.weather
        self.environment.change_weather_status()
        for agent in self.agents:
            if agent.flag_to_pits:
                agent.add_time_for_pits()
                agent.bike.select_configuration(self.environment)
                agent.flag_to_pits = False
            agent.update_agent_parameter(weather, self.environment.weather)
        if self.current_lap == self.laps - 1:
            print(Fore.BLUE + "\nUltima vuelta")
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

    def print_ranking(self):
        return Fore.MAGENTA + "\nResultados de la vuelta" + Fore.CYAN + " {}:\n".format(self.current_lap + 1) + \
            Fore.BLUE + "Posicion" + Fore.WHITE + " -" + Fore.CYAN + " Tiempo de Carrera" + Fore.WHITE + \
            " -" + Fore.GREEN + " Tiempo de Vuelta" + Fore.WHITE + "  -" + Fore.RED + " Piloto\n"

    def print_agent(self, agent):
        ranking = agent.ranking
        res = ""
        if 8 - number_digits(ranking) > 0:
            for j in range(8 - number_digits(ranking)):
                res += " "
        res += Fore.BLUE + "{}".format(ranking + 1) + Fore.WHITE + " -" + Fore.CYAN + " {}".format(
            seconds_to_minutes(agent.time_track)) + Fore.WHITE + " -" + Fore.GREEN + " {}".format(
            seconds_to_minutes(agent.time_lap)) + Fore.WHITE + " -" + Fore.RED + " {} con la {}".format(
            agent.rider.name, agent.bike.brand + " " + agent.bike.model) + "\n"
        agent.time_lap = 0
        return res

    def print_end_ranking(self):
        res = Fore.MAGENTA + "\nResultado final:\n"
        res += Fore.BLUE + "Posicion" + Fore.WHITE + " -" + Fore.CYAN + " Tiempo de Carrera" + Fore.WHITE + \
            " -" + Fore.RED + " Piloto\n"
        for agent in self.agents:
            res += self.print_end_agent(agent)
        return res

    def print_end_agent(self, agent):
        ranking = agent.ranking
        res = ""
        if 8 - number_digits(ranking) > 0:
            for j in range(8 - number_digits(ranking)):
                res += " "
        res += Fore.BLUE + "{}".format(ranking + 1) + Fore.WHITE + " -" + Fore.CYAN + " {}".format(
            seconds_to_minutes(agent.time_track)) + Fore.WHITE + " -" + Fore.RED + " {} con la {}".format(
            agent.rider.name, agent.bike.brand + " " + agent.bike.model) + "\n"
        agent.time_lap = 0
        return res
