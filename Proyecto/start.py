from pynput import keyboard
from os import name, system
from time import sleep
from sys import exit

from simulation.simulator import start


def main():
    print_welcome()
    keyboard.Listener(key).run()


def print_welcome():
    clear_console()
    print("Hola, bienvenido al simulador de Jefe Tecnico de Moto GP")
    print("Para Iniciar Nueva Simulacion Presione [N]")
    print("Para Salir del Simulador Presione [E]")


def clear_console():
    if name == "ce" or name == "nt" or name == "dos":
        system("cls")
    elif name == "posix":
        system("clear")


def key(tecla):
    if tecla == keyboard.KeyCode.from_char('n'):
        new_simulation()
        print_new_simulation()
    elif tecla == keyboard.KeyCode.from_char('e'):
        exit_()


def new_simulation():
    clear_console()
    print("Se ha iniciado una nueva simulacion....")
    test_simulation()


def test_simulation():
    print("\n\nSIMULACION:")
    time = 1  # Tiempo que demora la simulacion de una vuelta
    stop = False  # Reajustes en tiempo real
    start(time, stop)


def print_new_simulation():
    print("Para Iniciar Nueva Simulacion Presione [N]")
    print("Para Salir del Simulador Presione [E]")


def exit_():
    clear_console()
    print("Simulaciones terminadas")
    sleep(3)
    exit(0)


if __name__ == '__main__':
    main()
