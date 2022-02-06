from time import sleep
from simulation.race import Race

class Simulator:
    def start(self, race: Race):

        print("\nInicio de la carrera\n")

        while True:
            for section in race.environment.track.sections:
                for agent in race.agents:
                    agent.overcome_an_obstacle(section, race, race.environment.weather)
                print("La seccion {} ha sido superada".format(section[0]))
                race.ranking()
            if race.change_lap() or len(race.agents) == 0:
                race.ranking()
                break