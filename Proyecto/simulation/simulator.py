from simulation.race import Race


class Simulator:
    def start(self, race: Race):
        print("\nInicio de la carrera\n")
        while True:
            for section in race.environment.track.sections:
                for i in range(0, len(race.agents)):
                    if i == 0:
                        if not race.agents[i].overcome_an_obstacle(section, race, race.environment.weather, None,
                                                                   race.agents[i + 1]):
                            race.agents.remove(race.agents[i])
                            i -= 1
                        if race.agents[i].shot_down == 1:
                            race.agents.remove(race.agents[i + 1])
                    elif i == len(race.agents):
                        if not race.agents[i].overcome_an_obstacle(section, race, race.environment.weather,
                                                                   race.agents[i - 1], None):
                            race.agents.remove(race.agents[i])
                            i -= 1
                        if race.agents[i].shot_down == -1:
                            race.agents.remove(race.agents[i - 1])
                            i -= 1
                    else:
                        if not race.agents[i].overcome_an_obstacle(section, race, race.environment.weather,
                                                                   race.agents[i - 1], race.agents[i + 1]):
                            race.agents.remove(race.agents[i])
                            i -= 1
                        if race.agents[i].shot_down == 1:
                            race.agents.remove(race.agents[i + 1])
                        elif race.agents[i].shot_down == -1:
                            race.agents.remove(race.agents[i - 1])
                            i -= 1
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
