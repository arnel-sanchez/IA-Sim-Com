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
            print("\nCarrera terminada\n")
            self.print_ranking()
            return True
        elif self.current_lap == self.laps - 1:
            weather = self.environment.weather
            self.environment.change_weather_status()
            for agent in self.agents:
                if agent.flag_to_pits:
                    agent.add_time_for_pits()
                    agent.bike.select_configuration(self.environment)
                agent.update_agent_parameter(weather,self.environment.weather, self.environment.track.sections[0])
            print("\nUltima vuelta\n")
            self.print_ranking_lap()
            return False
        else:
            weather = self.environment.weather
            self.environment.change_weather_status()
            for agent in self.agents:
                if agent.flag_to_pits:
                    agent.add_time_for_pits()
                    agent.bike.select_configuration(self.environment)
                agent.update_agent_parameter(weather,self.environment.weather, self.environment.track.sections[0])
            print("\nVuelta {}\n".format(self.current_lap))
            self.print_ranking_lap()
            return False

    def print_ranking(self):
        i = 1
        print("Posicion - Tiempo de Carrera - Tiempo de Vuelta: Piloto")
        for x in self.rank:
            spaces = ""
            if 8 - number_digits(i) > 0:
                for j in range(8 - number_digits(i)):
                    spaces += " "
            print(
                spaces + "{} - {}  - {}: {} con la {}".format(i, seconds_to_minutes(x.time_track),
                                                              seconds_to_minutes(x.time_lap),
                                                              x.rider.name, x.bike.brand + " " + x.bike.model))
            i += 1
        print()

    def print_ranking_lap(self):
        i = 1
        print("Posicion - Tiempo Acumulado - Tiempo de Vuelta: Piloto")
        for x in self.rank:
            spaces = ""
            if 8 - number_digits(i) > 0:
                for j in range(8 - number_digits(i)):
                    spaces += " "
            print(spaces + "{} - {} - {}: {} con la {}".format(i, seconds_to_minutes(x.time_track),
                                                               seconds_to_minutes(x.time_lap),
                                                               x.rider.name, x.bike.brand + " " + x.bike.model))
            x.time_lap = 0
            i += 1
        print()

    def ranking(self):
        self.agents.sort(key=lambda agent: agent.time_track)
        self.agents[0].distance_to_nearest_behind = self.agents[0].time_track - self.agents[1].time_track
        for i in range(1, len(self.agents) - 1):
            self.agents[i].distance_to_nearest_forward = self.agents[i - 1].distance_to_nearest_behind
            self.agents[i].distance_to_nearest_behind = self.agents[i].time_track - self.agents[i + 1].time_track
            self.agents[i + 1].distance_to_nearest_forward = self.agents[i].distance_to_nearest_behind
