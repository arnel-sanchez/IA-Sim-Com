from os.path import dirname, abspath
from sys import path

SCRIPT_DIR = dirname(abspath(__file__))
path[0]=dirname(SCRIPT_DIR)
path[1]=dirname(SCRIPT_DIR)
from main import main

if __name__ == '__main__':
    main("Prueba15,#Error,Solo se pueden redefinir las variables turning_curves y driving_straight que pertenecen al tipo.pys")