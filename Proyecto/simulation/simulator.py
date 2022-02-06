from simulation.race import Race


class Simulator:
    def start(self, race: Race):
        print("\nInicio de la carrera\n")
        while True:
            for section in race.environment.track.sections:
                for agent in race.agents:
                    agent.overcome_an_obstacle(section, race, race.environment.weather)
                old_weather = race.emvironment.weather
                race.environment.change_weather()
                new_weather = race.environment.weather
                for agent in race.agents:
                    agent.update_agent_parameter(old_weather, new_weather, section)
                print("La seccion {} ha sido superada".format(section[0]))
                race.ranking()
            if race.change_lap() or len(race.agents) == 0:
                race.ranking()
                break
