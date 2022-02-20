from colorama import Fore
from heapq import heappop, heapify
from random import uniform

from simulation.race import Race, clear, printer


class Simulation:
    def __init__(self, race: Race):
        self.race = race

    def start(self):
        print(Fore.MAGENTA + "\nPista: " + Fore.CYAN + " {}".format(self.race.environment.track.name))
        self.race.environment.weather.print("Clima")
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
            
            if not self.race.environment.flag_change_weather:
                prob = uniform(0, 1)
            else:
               prob=self.race.environment.environments[self.race.environment.i].funciones[0].eval()
               if not (prob<=1 and prob>=0):
                   prob= uniform(0, 1)
                   
            if prob < 0.0005:
               self.race.environment.change_weather_status()

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
            self.race.environment.weather.print("Clima")
        print(Fore.BLUE + "\nCarrera terminada\n")
        printer(self.race.print_end())
        printer("\n")
