from os.path import dirname, abspath
from sys import path

SCRIPT_DIR = dirname(abspath(__file__))
path[0] = dirname(SCRIPT_DIR)
path[1] = dirname(SCRIPT_DIR)

from main import main

if __name__ == '__main__':
    main("Prueba9, #Error,No hay ninguna variable con este nombre accesible desde este ambito.pys")
