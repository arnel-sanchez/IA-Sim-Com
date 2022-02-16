from colorama import Fore

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
        self.flag_laps = False
        for agent in agents:
            agent.update_agent_initial_parameters(self.environment.weather)
            agent.bike.select_configuration(environment)

    def change_lap(self):
        self.flag_laps = False
        self.current_lap += 1
        if self.current_lap == self.laps:
            print(Fore.BLUE + "\nCarrera terminada")
            self.print_ranking()
            return True
        elif self.current_lap == self.laps - 1:
            weather = self.environment.weather
            self.environment.change_weather_status()
            for agent in self.agents:
                if agent.flag_to_pits:
                    agent.add_time_for_pits()
                    agent.bike.select_configuration(self.environment)
                agent.update_agent_parameter(weather, self.environment.weather)
            #print(Fore.BLUE + "\nUltima vuelta\n")
            self.print_ranking_lap()
            return False
        else:
            weather = self.environment.weather
            self.environment.change_weather_status()
            for agent in self.agents:
                if agent.flag_to_pits:
                    agent.add_time_for_pits()
                    agent.bike.select_configuration(self.environment)
                agent.update_agent_parameter(weather, self.environment.weather)
            self.print_ranking_lap()
            return False

    def end_lap(self):
        if not self.flag_laps:
            return False
        lap = self.agents[0].current_lap
        for x in self.agents:
            if x.current_lap != lap:
                return False
        return True

    def print_ranking(self):
        print(Fore.MAGENTA + "\nResultado final:")
        self.printer()

    def print_ranking_lap(self):
        print(Fore.MAGENTA + "\nResultados de la vuelta " + Fore.CYAN + "{}:".format(self.current_lap))
        self.printer()

    def printer(self):
        print(Fore.BLUE + "Posicion" + Fore.WHITE + " -" + Fore.CYAN + " Tiempo de Carrera" + Fore.WHITE + " -" +
              Fore.GREEN + " Tiempo de Vuelta:" + Fore.RED + " Piloto")
        i = 1
        for x in self.agents:
            spaces = ""
            if 8 - number_digits(i) > 0:
                for j in range(8 - number_digits(i)):
                    spaces += " "
            print(
                spaces + Fore.BLUE + "{}".format(i) + Fore.WHITE + " -" + Fore.CYAN +
                " {}".format(seconds_to_minutes(x.time_track)) + Fore.WHITE + " -" + Fore.GREEN +
                " {}:".format(seconds_to_minutes(x.time_lap)) + Fore.RED +
                " {} con la {}".format(x.rider.name, x.bike.brand + " " + x.bike.model))
            i += 1
        print()

    def ranking(self):
        if len(self.agents) < 2:
            return
        self.agents.sort(key=lambda agent: [-1 * agent.current_lap, -1 * agent.sections, agent.time_track])
        self.agents[0].distance_to_previous_rider = 0
        for i in range(1, len(self.agents) - 1):
            self.agents[i].distance_to_previous_rider = self.agents[i].time_track - self.agents[i - 1].time_track
            self.agents[i].distance_to_following_rider = self.agents[i + 1].time_track - self.agents[i].time_track
