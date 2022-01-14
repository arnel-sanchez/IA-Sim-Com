from time import sleep

from simulation.race import Race


def start(time: int, stop: bool, race: Race):
    print("\nPrimero se configura todo mediante DSL\n")

    print("\nInicio de la carrera\n")

    while True:        
        if race.change_lap():
            break
        
        sleep(time)

    print("\nFin de la carrera\n")
    race.ranking()