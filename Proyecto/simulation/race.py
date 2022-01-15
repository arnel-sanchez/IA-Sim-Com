from simulation.environment import Environment

class Race:
    def __init__(self, laps, agents, environment: Environment):
        self.agents = agents
        self.environment = environment
        self.laps = laps
        self.current_lap = 0
        self.rank = agents

    def change_lap(self):
        self.current_lap+=1
        if self.current_lap == self.laps:
            print("\nUltima vuelta\n")
            self.ranking()
            return True
        else:
            print("\nVuelta {}\n".format(self.current_lap))
            self.ranking()
            return False

    def ranking(self):
        i = 1
        for x in self.rank:
            print("{}: {}".format(i, x.rider.name))
            i+=1