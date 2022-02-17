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
        while number_digits(seconds) < 12:
            seconds = str(seconds) + "0"
        time = f"{minutes:02d}:0{seconds}"
    else:
        while number_digits(seconds) < 13:
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
                agent.update_agent_parameter(weather,self.environment.weather)
            print(Fore.BLUE + "\nUltima vuelta\n")
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
            res += Fore.MAGENTA + "Resultado final:\n"
            i = 1
            for x in self.agents:
                spaces = ""
                if 8 - number_digits(i) > 0:
                    for j in range(8 - number_digits(i)):
                        spaces += " "
                res += spaces + Fore.BLUE + "{}".format(i) + Fore.WHITE + " -" + Fore.CYAN + " {}".format(
                seconds_to_minutes(x.time_track)) + Fore.WHITE + " -" + Fore.GREEN + " {}:".format(
                seconds_to_minutes(x.time_lap)) + Fore.RED + " {} con la {}".format(
                x.rider.name, x.bike.brand + " " + x.bike.model) + "\n"
                i += 1
        else:
            res += Fore.MAGENTA + "Resultados de la vuelta" + Fore.CYAN + " {}:".format(self.current_lap + 1)+"\n"
        res += Fore.BLUE + "Posicion" + Fore.WHITE + " -" + Fore.CYAN + " Tiempo de Carrera" + Fore.WHITE + " -" + Fore.GREEN + " Tiempo de Vuelta:" + Fore.RED + " Piloto"
        return res

    def print_agent(self, agent):
        ranking = agent.ranking
        spaces = ""
        if 8 - number_digits(ranking) > 0:
            for j in range(8 - number_digits(ranking)):
                spaces += " "
        return spaces + Fore.BLUE + "{}".format(ranking) + Fore.WHITE + " -" + Fore.CYAN + " {}".format(
                seconds_to_minutes(agent.time_track)) + Fore.WHITE + " -" + Fore.GREEN + " {}:".format(
                seconds_to_minutes(agent.time_lap)) + Fore.RED + " {} con la {}".format(
                agent.rider.name, agent.bike.brand + " " + agent.bike.model) + "\n"