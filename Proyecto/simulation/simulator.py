from time import sleep
from simulation.race import Race

class Simulator:
    def start(self, time: int, stop: bool, race: Race):
        print("\nPrimero se configura todo mediante DSL\n")

        print("\nInicio de la carrera\n")

        while True:
            for section in race.environment.track.sections:
                for agent in race.agents:
                    agent.overcome_an_obstacle(section, race, race.environment.weather)
                print("\n")
                race.ranking()
            if race.change_lap() or len(race.agents) == 0:
                race.ranking()
                break
            sleep(time)