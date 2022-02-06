from simulation.race import Race


class Simulator:
    def start(self, race: Race):
        print("\nInicio de la carrera\n")
        while True:
            for section in race.environment.track.sections:
                for agent in race.agents:
                    agent.overcome_an_obstacle(section, race, race.environment.weather)
                old_weather = race.environment.weather
                race.environment.change_weather_params()
                new_weather = race.environment.weather
                for agent in race.agents:
                    agent.update_agent_parameter(old_weather, new_weather, section)
                if len(race.agents) != 0:
                    print("La seccion {} ha sido superada".format(section[0]))
                race.ranking()
            if race.change_lap() or len(race.agents) == 0:
                race.ranking()
                break
