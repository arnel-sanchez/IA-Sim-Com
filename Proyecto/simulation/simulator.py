from colorama import Fore

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
        for i in range(len(race.agents)):
            race.agents[i].ranking = i
        race.printer(race.print_ranking(False))
        end_lap = 0
        while True:
            k = 0
            while True:
                remove_agents = []
                while k < len(race.agents):
                    if not race.agents[k].turn_done:
                        break
                    k += 1
                if k == len(race.agents):
                    break
                if race.current_lap == race.laps:
                    race.clear()
                    race.printer(race.print_ranking(True))
                if end_lap == len(race.agents):
                    race.clear()
                    end_lap = 0
                    race.printer(race.print_ranking(False))
                if not race.agents[k].turn_done:
                    race.agents[k].turn_done = True
                if not race.agents[k].overcome_an_obstacle(race):
                    remove_agents.append(race.agents[k])
                else:
                    if race.agents[k].sections == len(race.environment.track.sections) - 1:
                        race.flag_laps = True
                        race.agents[k].change_section(race.environment.track.sections[0], True)
                        race.printer(race.print_agent(race.agents[k]))
                        end_lap += 1
                    else:
                        race.agents[k].change_section(race.environment.track.sections[race.agents[k].sections + 1],
                                                      False)
                if race.agents[k].shot_down is not None:
                    remove_agents.append(race.agents[k].shot_down)
                    race.agents[k].shot_down = None
                if len(remove_agents) > 0:
                    for ra in remove_agents:
                        k -= 1
                        race.agents.remove(ra)
                    if len(race.agents) < 1:
                        print(Fore.BLUE + "\nNingun piloto ha terminado la carrera.\n")
                        return
                    for i in range(len(race.agents)):
                        race.agents[i].ranking = i
            for a in race.agents:
                a.turn_done = False
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
        print(Fore.MAGENTA + "\nClima:")
        print(Fore.CYAN + "Estado: {}".format(translate_weather[weather.weather_status.value]))
        print(Fore.CYAN + "Humedad: {}".format(self.measure(weather.humidity)))
        print(Fore.CYAN + "Temperatura: {}".format(self.measure(weather.temperature)))
        print(Fore.CYAN + "Visibilidad: {}".format(self.measure(weather.visibility)))
        print(Fore.CYAN + "Viento: {}, Intensidad {}\n".format(translate_direction[weather.wind.value],
                                                               self.measure(weather.wind_intensity)))

    def measure(self, number):
        return "Alta" if number > 6 else "Baja" if number < 4 else "Media"
