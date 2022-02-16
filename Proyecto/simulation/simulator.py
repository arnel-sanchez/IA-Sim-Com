from colorama import Fore
from heapq import heappush, heappop, heapify

from simulation.race import Race


class Simulator:
    def start(self, race: Race):
        print(Fore.MAGENTA + "\nPista: " + Fore.CYAN + "{}\n".format(race.environment.track.name))
        self.print_race(race)
        print(Fore.MAGENTA + "Pilotos:")
        for i in range(len(race.agents)):
            print(Fore.CYAN + "{} - {} con la {}".format(i + 1, race.agents[i].rider.name,
                                                         race.agents[i].bike.brand + " " + race.agents[i].bike.model))
        print(Fore.BLUE + "\nInicio de la carrera\n")
        print(Fore.MAGENTA + "Vuelta " + Fore.CYAN + "1:")
        h = []
        for x in race.agents:
            heappush(h, x)
        while True:
            agent = heappop(h)
            i = 0
            for a in race.agents:
                if a == agent:
                    break
                i += 1
            previous_agent = None
            if i > 0:
                previous_agent = race.agents[i - 1]
            following_agent = None
            if i < len(race.agents) - 1:
                following_agent = race.agents[i + 1]
            if not agent.overcome_section(race, following_agent, previous_agent):
                race.agents.remove(agent)
            else:
                if race.agents[i].sections == len(race.environment.track.sections) - 1:
                    race.flag_laps = True
                    race.agents[i].change_section(race.environment.track.sections[0], True)
                else:
                    race.agents[i].change_section(race.environment.track.sections[race.agents[i].sections + 1],
                                                  False)
                heappush(h, agent)
            if agent.previous_shot_down:
                race.agents.remove(previous_agent)
                h.remove(previous_agent)
                heapify(h)
            if agent.following_shot_down:
                race.agents.remove(following_agent)
                h.remove(following_agent)
                heapify(h)
            if len(h) < 1:
                print(Fore.BLUE + "\nNingun piloto ha terminado la carrera.\n")
                break
            race.ranking()
            if race.end_lap():
                if race.change_lap():
                    break
                old_weather = race.environment.weather
                race.environment.change_weather_params()
                new_weather = race.environment.weather
                for agent in race.agents:
                    agent.update_agent_parameter(old_weather, new_weather)
                self.print_race(race)
                print(Fore.MAGENTA + "Vuelta " + Fore.CYAN + "{}:".format(race.current_lap + 1))

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
