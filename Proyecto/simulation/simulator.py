from simulation.race import Race
from colorama import init, Fore


class Simulator:
    def start(self, race: Race):
        print(Fore.MAGENTA + "\nPista: " + Fore.CYAN + " {}".format(race.environment.track.name))
        self.print_race(race)
        print(Fore.MAGENTA + "Pilotos:")
        for i in range(len(race.rank)):
            print(Fore.CYAN+"{} - {} con la {}".format(i + 1, race.rank[i].rider.name,
                                                       race.rank[i].bike.brand + " " + race.rank[i].bike.model))
        print("\n" + Fore.BLUE + "Inicio de la carrera\n")
        while True:
            if race.current_lap < race.laps - 1:
                print(Fore.CYAN + "Vuelta {}:".format(race.current_lap + 1))
            else:
                print(Fore.CYAN + "Ultima vuelta:")
            for section in race.environment.track.sections:
                print("\n" + Fore.BLUE + "-> Inicia la seccion {}.".format(section[0]))
                remove_agents = set()
                for i in range(len(race.agents)):
                    if remove_agents.__contains__(race.agents[i]):
                        continue
                    if len(race.agents) == 1:
                        if not race.agents[i].overcome_an_obstacle(section, race, None, None):
                            remove_agents.add(race.agents[i])
                    else:
                        forward_agent = None
                        if i > 0 and not remove_agents.__contains__(race.agents[i - 1]):
                            forward_agent = race.agents[i - 1]
                        behind_agent = None
                        if i < len(race.agents) - 1 and not remove_agents.__contains__(race.agents[i + 1]):
                            behind_agent = race.agents[i + 1]
                        if not race.agents[i].overcome_an_obstacle(section, race, forward_agent, behind_agent):
                            remove_agents.add(race.agents[i])
                    if race.agents[i].shot_down == 1:
                        remove_agents.add(race.agents[i + 1])
                    elif race.agents[i].shot_down == -1:
                        remove_agents.add(race.agents[i - 1])
                for x in remove_agents:
                    race.agents.remove(x)
                if len(race.agents) > 0:
                    print(Fore.BLUE + "-> La seccion {} ha sido superada.".format(section[0]))
                    if len(race.agents) > 1:
                        race.ranking()
                else:
                    break
                old_weather = race.environment.weather
                race.environment.change_weather_params()
                new_weather = race.environment.weather
                for agent in race.agents:
                    agent.update_agent_parameter(old_weather, new_weather, section)
            if len(race.agents) == 0:
                print("\n" + Fore.BLUE + "Ningun piloto ha terminado la carrera.\n")
                break
            if race.change_lap():
                race.ranking()
                break
            else:
                self.print_race(race)

    def print_race(self, race: Race):
        weather = race.environment.weather
        translate_weather = ["Soleado", "Nublado", "Lluvioso"]
        translate_direction = ["Norte", "Noreste", "Este", "Sureste", "Sur", "Suroeste", "Oeste", "Noroeste"]
        print("\n" + Fore.MAGENTA + "Clima:")
        print(Fore.CYAN + "Estado: {}".format(translate_weather[weather.weather_status.value]))
        print(Fore.CYAN + "Humedad: {}".format(self.rank(weather.humidity)))
        print(Fore.CYAN + "Temperatura: {}".format(self.rank(weather.temperature)))
        print(Fore.CYAN + "Visibilidad: {}".format(self.rank(weather.visibility)))
        print(Fore.CYAN + "Viento: {}".format(translate_direction[weather.wind.value]))
        print(Fore.CYAN + "Intensidad del viento: {}\n".format(self.rank(weather.wind_intensity)))

    def rank(self, number):
        return "Alta" if number > 6 else "Baja" if number < 4 else "Media"
