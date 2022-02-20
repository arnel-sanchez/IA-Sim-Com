from colorama import Fore
from heapq import heappop, heapify

from simulation.race import Race, clear, printer


def measure(number):
    return "Alta" if number > 6 else "Baja" if number < 4 else "Media"


class Simulation:
    def __init__(self, race: Race):
        self.translate_weather = ["Soleado", "Nublado", "Lluvioso"]
        self.translate_direction = ["Norte", "Noreste", "Este", "Sureste", "Sur", "Suroeste", "Oeste", "Noroeste"]
        self.race = race

    def start(self):
        print(Fore.MAGENTA + "\nPista: " + Fore.CYAN + " {}".format(self.race.environment.track.name))
        self.print()
        print(Fore.MAGENTA + "Pilotos:")
        for i in range(len(self.race.ranking)):
            print(Fore.CYAN + "{} - {} con la {}".format(i + 1, self.race.ranking[i].rider.name,
                                                         self.race.ranking[i].bike.brand + " " +
                                                         self.race.ranking[i].bike.model))
        print(Fore.BLUE + "\nInicio de la carrera\n")
        for i in range(len(self.race.agents)):
            self.race.agents[i].ranking = i
        clear()
        printer(self.race.print())
        end_lap = 0
        heap = [a for a in self.race.agents]
        while True:
            agent = None
            while len(heap) > 0:
                agent = heappop(heap)
                if not agent.off_road:
                    break
                if agent.current_lap == self.race.laps:
                    print(Fore.LIGHTWHITE_EX + "El piloto {} ha terminado la carrera.".format(agent.rider.name))
                    printer(agent.print())
                agent = None
            if agent is None:
                break
            if agent.current_lap > 0 and agent.sections == 0:
                printer(agent.print())
                end_lap += 1
            if end_lap == len(self.race.agents):
                end_lap = 0
                printer(self.race.print())
            remove_agents = []
            if agent.overcome_section(self.race):
                if agent.change_section(self.race):
                    self.race.flag_laps = True
                    if agent.current_lap == self.race.laps:
                        agent.off_road = True
                if not agent.review(self.race):
                    remove_agents.append(agent)
            else:
                remove_agents.append(agent)
            if agent.shot_down is not None:
                remove_agents.append(agent.shot_down)
                agent.shot_down = None
            if len(remove_agents) > 0:
                for ra in remove_agents:
                    self.race.agents.remove(ra)
                    if ra != agent:
                        heap.remove(ra)
                if len(self.race.agents) < 1:
                    print(Fore.LIGHTWHITE_EX + "\nNingun piloto ha terminado la carrera.")
                    break
                for i in range(len(self.race.agents)):
                    self.race.agents[i].ranking = i
            if not agent.off_road or agent.current_lap == self.race.laps:
                heap.append(agent)
            heapify(heap)
            if not self.race.end_lap() or self.race.change_lap():
                continue
            old_weather = self.race.environment.weather
            self.race.environment.change_weather_params()
            new_weather = self.race.environment.weather
            for agent in self.race.agents:
                agent.update_agent_parameter(old_weather, new_weather)
            self.print()
        print(Fore.BLUE + "\nCarrera terminada\n")
        printer(self.race.print_end())
        printer("\n")

    def print(self):
        weather = self.race.environment.weather
        print(Fore.MAGENTA + "\nClima:")
        print(Fore.CYAN + "Estado: {}".format(self.translate_weather[weather.weather_status.value]))
        print(Fore.CYAN + "Humedad: {}".format(measure(weather.humidity)))
        print(Fore.CYAN + "Temperatura: {}".format(measure(weather.temperature)))
        print(Fore.CYAN + "Visibilidad: {}".format(measure(weather.visibility)))
        print(Fore.CYAN + "Viento: {}, Intensidad {}\n".format(self.translate_direction[weather.wind.value],
                                                               measure(weather.wind_intensity)))
