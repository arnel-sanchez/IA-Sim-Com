from colorama import Fore
from heapq import heappush, heappop, heapify

from simulation.race import Race


class Simulator:
    def start(self, race: Race):
        race.clear()
        print(Fore.MAGENTA + "\nPista: " + Fore.CYAN + " {}\n".format(race.environment.track.name))
        self.print_race(race)
        print(Fore.MAGENTA + "Pilotos:")
        for i in range(len(race.rank)):
            print(Fore.CYAN + "{} - {} con la {}".format(i + 1, race.rank[i].rider.name,
                                                         race.rank[i].bike.brand + " " + race.rank[i].bike.model))
        print(Fore.BLUE + "\nInicio de la carrera\n")
        h = []
        for i in range(len(race.agents)):
            race.agents[i].rank = i
            heappush(h, race.agents[i])
        race.printer(race.print_ranking(False))
        end_lap = 0
        while True:
            if race.current_lap == race.laps:
                race.clear()
                race.printer(race.print_ranking(True))
            if end_lap == len(race.agents):
                race.clear()
                end_lap = 0
                race.printer(race.print_ranking(False))
            agent = heappop(h)
            remove_agents = []
            if not agent.overcome_an_obstacle(race):
                remove_agents.append(agent)
            if agent.shot_down is not None:
                remove_agents.append(agent.shot_down)
                agent.shot_down = None
            if not remove_agents.__contains__(agent):
                heappush(h, agent)
            for ra in remove_agents:
                if ra != agent:
                    h.remove(ra)
                race.agents.remove(ra)
            if len(h) < 1:
                print(Fore.BLUE + "\nNingun piloto ha terminado la carrera.\n")
                break
            if race.end_lap():
                if race.change_lap():
                    break
                old_weather = race.environment.weather
                race.environment.change_weather_params()
                new_weather = race.environment.weather
                for agent in race.agents:
                    agent.update_agent_parameter(old_weather, new_weather)
                self.print_race(race)
            if len(remove_agents) > 0:
                heapify(h)

    def print_race(self, race: Race):
        weather = race.environment.weather
        translate_weather = ["Soleado", "Nublado", "Lluvioso"]
        translate_direction = ["Norte", "Noreste", "Este", "Sureste", "Sur", "Suroeste", "Oeste", "Noroeste"]
        print(Fore.MAGENTA + "Clima:")
        print(Fore.CYAN + "Estado: {}".format(translate_weather[weather.weather_status.value]))
        print(Fore.CYAN + "Humedad: {}".format(self.rank(weather.humidity)))
        print(Fore.CYAN + "Temperatura: {}".format(self.rank(weather.temperature)))
        print(Fore.CYAN + "Visibilidad: {}".format(self.rank(weather.visibility)))
        print(Fore.CYAN + "Viento: {}, Intensidad {}\n".format(translate_direction[weather.wind.value],
                                                               self.rank(weather.wind_intensity)))

    def rank(self, number):
        return "Alta" if number > 6 else "Baja" if number < 4 else "Media"
