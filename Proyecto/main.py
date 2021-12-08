from compilation.tokenizer import Tokenizer
from simulation.simulator import start


def test_simulation():
    print("\n\nSIMULACION:")
    time = 3  # Tiempo que demora la simulacion de una vuelta
    stop = False  # Reajustes en tiempo real
    start(time, stop)


def main():
    test_simulation()


if __name__ == '__main__':
    main()
