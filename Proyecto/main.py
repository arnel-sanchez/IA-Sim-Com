from compilation.tokenizer import Tokenizer
from simulation.simulator import start
import os
import sys
from pynput import keyboard
from time import sleep

def test_simulation():
    print("\n\nSIMULACION:")
    time = 1  # Tiempo que demora la simulacion de una vuelta
    stop = False  # Reajustes en tiempo real
    start(time, stop)

def print_welcome():
    clear_console()
    print("Hola, bienvenido al simulador de Jefe Tecnico de Moto GP")
    print("Para Iniciar Nueva Simulacion Presione [N]")
    print("Para Salir del Simulador Presione [E]")

def print_new_simulation():
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
        exit()

def new_simulation():
    clear_console()
    print("Se ha iniciado una nueva simulacion....")
    test_simulation()

def exit():
    clear_console()
    print("Simulaciones terminadas")
    sleep(3)
    sys.exit()

def clear_console():
    if os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")

if __name__ == '__main__':
    main()