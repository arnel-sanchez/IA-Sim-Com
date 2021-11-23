from time import sleep

from simulation.race import race
from simulation.crew_chief import default_crew_chiefs


def start(time: int, stop: bool):
    print("\nPrimero se configura todo mediante DSL\n")

    r = race()
    print("Pista: {}".format(r.track.name))
    r.weather.print_weather()

    print("\nEquipos:")
    crew_chiefs = default_crew_chiefs()
    i = 1
    for cc in crew_chiefs:
        print("{}:".format(i))
        i += 1
        crew_chiefs[cc].print_crew_chief()
        crew_chiefs[cc].pilot.print_pilot()
        crew_chiefs[cc].pilot.motorcycle.print_motorcycle()
        print()

    print("\nInicio de la carrera\n")

    while True:
        print("Faltan {} vuelta{}".format(r.laps, "s" if r.laps > 1 else "") if r.laps > 0 else "Ultima vuelta")

        print("Aqui va la Simulacion")

        r.laps -= 1
        if r.laps < 0:
            break
        sleep(time)

        if stop:
            print("\nPosibilidad de re-configurar en tiempo real mediante DSL")
            settings = input("Ajustes:")
            print(settings)

        print("\nAqui va la lista de ajustes hechos")

    print("\nFin de la carrera\n")
    print("Aqui van los resultados de la carrera\n")
