from simulation.race import Race


class Simulator:
    def start(self, race: Race):
        print("\nPista: {}".format(race.environment.track.name))
        print("\nClima:")
        print("Estado: {}".format(race.environment.weather.weather_status))
        print("Humedad: {}".format(race.environment.weather.humidity))
        print("Temperatura: {}".format(race.environment.weather.temperature))
        print("Visibilidad: {}".format(race.environment.weather.visibility))
        print("Viento: {}".format(race.environment.weather.wind))
        print("Intensidad del Viento: {}".format(race.environment.weather.wind_intensity))
        print("\nPilotos:")
        for i in range(len(race.rank)):
            print("{} - {} con la {}".format(i + 1, race.rank[i].rider.name,
                                             race.rank[i].bike.brand + " " + race.rank[i].bike.model))
        print("\nInicio de la carrera\n")
        while True:
            for section in race.environment.track.sections:
                remove_agents = set()
                for i in range(0, len(race.agents)):
                    if i == 0:
                        if len(race.agents) > 1 and not race.agents[i].overcome_an_obstacle(
                                section, race, None, race.agents[i + 1]):
                            remove_agents.add(race.agents[i])
                        elif len(race.agents) == 1 and not race.agents[i].overcome_an_obstacle(
                                section, race, None, None):
                            remove_agents.add(race.agents[i])
                        if race.agents[i].shot_down == 1:
                            remove_agents.add(race.agents[i + 1])
                    elif len(race.agents) > 1 and i == len(race.agents)-1:
                        if not race.agents[i].overcome_an_obstacle(section, race, race.agents[i - 1], None):
                            remove_agents.add(race.agents[i])
                        elif len(race.agents) == 1 and not race.agents[i].overcome_an_obstacle(section, race, None,
                                                                                               None):
                            remove_agents.add(race.agents[i])
                        if race.agents[i].shot_down == -1:
                            remove_agents.add(race.agents[i - 1])
                    elif len(race.agents) > 1:
                        if not race.agents[i].overcome_an_obstacle(section, race, race.agents[i - 1],
                                                                   race.agents[i + 1]):
                            remove_agents.add(race.agents[i])
                        if race.agents[i].shot_down == 1:
                            remove_agents.add(race.agents[i + 1])
                        elif race.agents[i].shot_down == -1:
                            remove_agents.add(race.agents[i - 1])
                for x in remove_agents:
                    race.agents.remove(x)
                old_weather = race.environment.weather
                race.environment.change_weather_params()
                new_weather = race.environment.weather
                for agent in race.agents:
                    agent.update_agent_parameter(old_weather, new_weather, section)
                if len(race.agents) != 0:
                    print("La seccion {} ha sido superada".format(section[0]))
                    if len(race.agents) > 1:
                        race.ranking()
                else:
                    break
            if len(race.agents) == 0:
                break

            if race.change_lap():
                race.ranking()
                break
            else:
                print("\nClima:")
                print("Estado: {}".format(race.environment.weather.weather_status))
                print("Humedad: {}".format(race.environment.weather.humidity))
                print("Temperatura: {}".format(race.environment.weather.temperature))
                print("Visibilidad: {}".format(race.environment.weather.visibility))
                print("Viento: {}".format(race.environment.weather.wind))
                print("Intensidad del Viento: {}".format(race.environment.weather.wind_intensity))