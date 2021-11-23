from compilation.tokenizer import Tokenizer
from simulation.simulator import start


def test_tokenizer():
    print("\nCOMPILACION:\n")
    tokenizer = Tokenizer()
    file, text = "console", "if;point else point22; 22 3.4; point_1 point;\"AAA\"aaa\n123.0 _a.a"
    print(text)
    tokens, error = tokenizer.tokenize(file, text)
    print()
    if error is not None:
        print(error)
    else:
        for token in tokens:
            print(token)


def test_simulation():
    print("\n\nSIMULACION:")
    time = 3  # Tiempo que demora la simulacion de una vuelta
    stop = False  # Reajustes en tiempo real
    start(time, stop)


def main():
    test_tokenizer()
    test_simulation()


if __name__ == '__main__':
    main()
