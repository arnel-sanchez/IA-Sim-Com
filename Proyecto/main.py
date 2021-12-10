from compilation.tokenizer import Tokenizer
from simulation.simulator import start
from os import name, system
from sys import exit
from pynput import keyboard


def test_simulation():
    print("\n\nSIMULACION:")
    time = 3  # Tiempo que demora la simulacion de una vuelta
    stop = False  # Reajustes en tiempo real
    start(time, stop)


def print_welcome():
    clear_console()
    print("Hola, bienvenido al simulador de Jefe Tecnico de Moto GP")
    print("Para Iniciar Nueva Simulacion Presione [N]")
    print("Para Salir del Simulador Presione [E]")


def print_new_simulation():
    clear_console()
    print("Para Iniciar Nueva Simulacion Presione [N]")
    print("Para Salir del Simulador Presione [E]")


def main():
    print_welcome()
    keyboard.Listener(key).run()


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


def exit_():
    clear_console()
    print("Simulaciones terminadas")
    exit(0)


def clear_console():
    if name == "ce" or name == "nt" or name == "dos":
        system("cls")
    elif name == "posix":
        system("clear")


if __name__ == '__main__':
    main()
