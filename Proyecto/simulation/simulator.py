from time import sleep
from math import pow
from math import sqrt
from simulation.race import Race

class Simulator:
    def start(time: int, stop: bool, race: Race):
        print("\nPrimero se configura todo mediante DSL\n")

        print("\nInicio de la carrera\n")

        while True:
            for section in race.environment.track.sections:
                for agent in race.agents:
                    if Simulator.overcome_an_obstacle(section, agent):
                        print("Obstaculo {} superado".format(section[0]))
                    else:
                        print("El piloto {} ha perdido el control de su moto".format(agent.rider.name))
                        race.agents.remove(agent)
            if race.change_lap():
                break
            
            sleep(time)

        print("\nFin de la carrera\n")
        race.ranking()

    def overcome_an_obstacle(section, agent):
        #Primer Análisis
        #Cuando entra a la sección se hace un cálculo para sacar la conclusión de qué acción sería la mejor para ejecutar
        agent.aceleration = agent.bike.Simulator.discrete_variable_generator()
        vf = sqrt(pow(agent.speed) + 2 * section[2]*agent.aceleration)
        t = (vf - agent.speed)/agent.aceleration
        agent.time_lap += t
        agent.speed = vf

        #Segundo Análisis
        #Cuando se va a salir de la sección se hace una reestructuración del ranking

        return

    def continuous_variable_generator():
        return 5

    def discrete_variable_generator():
        return 5