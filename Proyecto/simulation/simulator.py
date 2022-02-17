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
        for x in race.agents:
            heappush(h, x)
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
            if len(race.agents) == 1:
                if not race.agents[0].overcome_an_obstacle(race, None, None):
                    remove_agents.append(race.agents[0])
            else:
                i = 0
                for j in range(len(race.agents)):
                    if race.agents[j] == agent:
                        i = j
                        break
                if i == 0:
                    if not race.agents[i].overcome_an_obstacle(race, None, race.agents[i + 1]):
                        if race.agents[i].shot_down_behind:
                            remove_agents.append(race.agents[i + 1])
                        remove_agents.append(race.agents[i])
                    else:
                        if race.agents[i].sections == len(race.environment.track.sections) - 1:
                            race.flag_laps = True
                            race.agents[i].change_section(race.environment.track.sections[0], True)
                            race.printer(race.print_agent(race.agents[i], i+1))
                            end_lap += 1
                        else:
                            race.agents[i].change_section(race.environment.track.sections[race.agents[i].sections + 1], False)
                elif i == len(race.agents) - 1:
                    if not race.agents[i].overcome_an_obstacle(race, race.agents[i - 1], None):
                        if race.agents[i].shot_down_forward:
                            remove_agents.append(race.agents[i - 1])
                        remove_agents.append(race.agents[i])
                    else:
                        if race.agents[i].sections == len(race.environment.track.sections) - 1:
                            race.flag_laps = True
                            race.agents[i].change_section(race.environment.track.sections[0], True)
                            race.printer(race.print_agent(race.agents[i], i+1))
                            end_lap += 1
                        else:
                            race.agents[i].change_section(race.environment.track.sections[race.agents[i].sections + 1], False)
                else:
                    if not race.agents[i].overcome_an_obstacle(race, race.agents[i - 1],
                                                               race.agents[i + 1]):
                        if race.agents[i].shot_down_forward:
                            remove_agents.append(race.agents[i - 1])
                        if race.agents[i].shot_down_behind:
                            remove_agents.append(race.agents[i + 1])
                        remove_agents.append(race.agents[i])
                    else:
                        if race.agents[i].sections == len(race.environment.track.sections) - 1:
                            race.flag_laps = True
                            race.agents[i].change_section(race.environment.track.sections[0], True)
                            race.printer(race.print_agent(race.agents[i], i+1))
                            end_lap += 1
                        else:
                            race.agents[i].change_section(race.environment.track.sections[race.agents[i].sections + 1], False)
            if len(remove_agents) != 0:
                for remove in remove_agents:
                    if remove != agent:
                        heappush(h, agent)
                        race.agents.remove(remove)
                    else:
                        race.agents.remove(remove)
            else:
                heappush(h, agent)
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
