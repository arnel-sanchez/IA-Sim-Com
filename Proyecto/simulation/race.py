from colorama import init, Fore

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
        self.rank = agents
        for agent in agents:
            agent.update_agent_initial_parameters(self.environment.weather, self.environment.track.sections[0])
            agent.bike.select_configuration(environment)

    def change_lap(self):
        self.current_lap += 1
        if self.current_lap == self.laps:
            print("\n" + Fore.BLUE + "Carrera terminada")
            self.print_ranking()
            return True
        else:
            weather = self.environment.weather
            self.environment.change_weather_status()
            for agent in self.agents:
                if agent.flag_to_pits:
                    agent.add_time_for_pits()
                    agent.bike.select_configuration(self.environment)
                agent.update_agent_parameter(weather, self.environment.weather, self.environment.track.sections[0])
            self.print_ranking_lap()
            return False

    def print_ranking_lap(self):
        print("\n" + Fore.MAGENTA + "Resultados de la vuelta" + Fore.CYAN + " {}:".format(self.current_lap))
        self.printer()

    def printer(self):
        print(Fore.BLUE + "Posicion" + Fore.WHITE + " - " + Fore.CYAN + "Tiempo de Carrera" + Fore.WHITE + " - " +
              Fore.GREEN + "Tiempo de Vuelta: " + Fore.RED + "Piloto")
        i = 1
        for x in self.rank:
            spaces = ""
            if 8 - number_digits(i) > 0:
                for j in range(8 - number_digits(i)):
                    spaces += " "
            print(spaces + Fore.BLUE + str(i) + Fore.WHITE + " - " + Fore.CYAN + seconds_to_minutes(x.time_track) +
                  Fore.WHITE + " - " + Fore.GREEN + seconds_to_minutes(x.time_lap) + ": " + Fore.RED +
                  "{} con la {} {}".format(x.rider.name, x.bike.brand, x.bike.model))
            i += 1
        print()

    def print_ranking(self):
        print("\n" + Fore.MAGENTA + "Resultado final:")
        self.printer()

    def ranking(self):
        self.agents.sort(key=lambda agent: agent.time_track)
        if len(self.agents) < 2:
            return
        self.agents[0].distance_to_nearest_forward = 0
        for i in range(1, len(self.agents) - 1):
            self.agents[i].distance_to_nearest_forward = self.agents[i].time_track - self.agents[i - 1].time_track
            self.agents[i].distance_to_nearest_behind = self.agents[i + 1].time_track - self.agents[i].time_track
