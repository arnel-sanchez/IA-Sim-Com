from colorama import Fore
from heapq import heapify, heappop

from simulation.race import Race


class Simulator:
    def start(self, race: Race):
        print(Fore.MAGENTA + "\nPista: " + Fore.CYAN + " {}".format(race.environment.track.name))
        self.print_race(race)
        print(Fore.MAGENTA + "Pilotos:")
        for i in range(len(race.ranking)):
            print(Fore.CYAN + "{} - {} con la {}".format(i + 1, race.ranking[i].rider.name,
                                                         race.ranking[i].bike.brand + " " + race.ranking[i].bike.model))
        print(Fore.BLUE + "\nInicio de la carrera\n")
        for i in range(len(race.agents)):
            race.agents[i].ranking = i
        race.clear()
        race.printer(race.print_ranking(False))
        end_lap = 0
        heap = [a for a in race.agents]
        while True:
            agent = None
            while len(heap) > 0:
                agent = heappop(heap)
                if not agent.off_road:
                    break
                if race.current_lap == race.laps - 1:
                    race.printer(race.print_agent(agent))
                agent = None
            if agent is None:
                break
            if agent.current_lap > 0 and agent.sections == 0:
                race.printer(race.print_agent(agent))
                end_lap += 1
                if agent.current_lap == race.laps:
                    race.agents.remove(agent)
            if end_lap == len(race.agents):
                end_lap = 0
                race.printer(race.print_ranking(race.current_lap == race.laps - 1))
            remove_agents = []
            if not agent.overcome_section(race):
                remove_agents.append(agent)
            else:
                if agent.sections == len(race.environment.track.sections) - 1:
                    race.flag_laps = True
                    agent.change_section(race.environment.track.sections[0], True)
                    if agent.current_lap == race.laps:
                        agent.off_road = True
                else:
                    agent.change_section(race.environment.track.sections[agent.sections + 1], False)
            if agent.shot_down is not None:
                remove_agents.append(agent.shot_down)
                agent.shot_down = None
            if len(remove_agents) > 0:
                for ra in remove_agents:
                    race.agents.remove(ra)
                    if ra != agent:
                        heap.remove(ra)
                if len(race.agents) < 1:
                    print(Fore.BLUE + "\nNingun piloto ha terminado la carrera.\n")
                    return
                for i in range(len(race.agents)):
                    race.agents[i].ranking = i
            if not agent.off_road:
                agent.review(race)
                heap.append(agent)
            heapify(heap)
            if not race.end_lap() or race.change_lap():
                continue
            old_weather = race.environment.weather
            race.environment.change_weather_params()
            new_weather = race.environment.weather
            for agent in race.agents:
                agent.update_agent_parameter(old_weather, new_weather)
            self.print_race(race)
        for agent in race.agents:
            race.printer(race.print_agent(agent))
        race.printer("\n")

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
