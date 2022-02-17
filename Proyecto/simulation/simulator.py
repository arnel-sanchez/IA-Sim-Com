from colorama import Fore
from heapq import heappush, heappop, heapify

from simulation.race import Race


class Simulator:
    def start(self, race: Race):
        race.clear()
        print(Fore.MAGENTA + "\nPista: " + Fore.CYAN + " {}".format(race.environment.track.name))
        self.print_race(race)
        print(Fore.MAGENTA + "Pilotos:")
        for i in range(len(race.ranking)):
            print(Fore.CYAN + "{} - {} con la {}".format(i + 1, race.ranking[i].rider.name,
                                                         race.ranking[i].bike.brand + " " + race.ranking[i].bike.model))
        print(Fore.BLUE + "\nInicio de la carrera\n")
        heap = []
        for i in range(len(race.agents)):
            race.agents[i].ranking = i
            heappush(heap, race.agents[i])
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
            agent = heappop(heap)
            remove_agents = []
            if not agent.overcome_an_obstacle(race):
                remove_agents.append(agent)
            else:
                if agent.sections == len(race.environment.track.sections) - 1:
                    race.flag_laps = True
                    agent.change_section(race.environment.track.sections[0], True)
                    race.printer(race.print_agent(agent))
                    end_lap += 1
                else:
                    agent.change_section(race.environment.track.sections[agent.sections + 1], False)
            if agent.shot_down is not None:
                remove_agents.append(agent.shot_down)
                agent.shot_down = None
            if not remove_agents.__contains__(agent):
                heappush(heap, agent)
            if len(remove_agents) > 0:
                for ra in remove_agents:
                    if ra != agent:
                        heap.remove(ra)
                    race.agents.remove(ra)
                if len(heap) < 1:
                    print(Fore.BLUE + "\nNingun piloto ha terminado la carrera.\n")
                    break
                for i in range(len(race.agents)):
                    race.agents[i].ranking = i
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
                heapify(heap)

    def print_race(self, race: Race):
        weather = race.environment.weather
        translate_weather = ["Soleado", "Nublado", "Lluvioso"]
        translate_direction = ["Norte", "Noreste", "Este", "Sureste", "Sur", "Suroeste", "Oeste", "Noroeste"]
        print(Fore.MAGENTA + "\nClima:")
        print(Fore.CYAN + "Estado: {}".format(translate_weather[weather.weather_status.value]))
        print(Fore.CYAN + "Humedad: {}".format(self.ranking(weather.humidity)))
        print(Fore.CYAN + "Temperatura: {}".format(self.ranking(weather.temperature)))
        print(Fore.CYAN + "Visibilidad: {}".format(self.ranking(weather.visibility)))
        print(Fore.CYAN + "Viento: {}, Intensidad {}\n".format(translate_direction[weather.wind.value],
                                                               self.ranking(weather.wind_intensity)))

    def ranking(self, number):
        return "Alta" if number > 6 else "Baja" if number < 4 else "Media"
