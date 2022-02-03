from compilation.tokenizer import Tokenizer
from compilation.utils import split_lines
from compilation.parser import *
from simulation.simulator import start


def test_compilation():
    print("\nCOMPILACION:\n")
    tokenizer = Tokenizer()
    file, text = "console", "point else point22; 22 3.4; point_1 point;\"AAA\"aaa\nif;123.0 _a.a"
    print(text)
    tokens, error = tokenizer.tokenize(file, text)
    print()
    if error is not None:
        print(error)
    else:
        for token in tokens:
            print(token)

    lines = split_lines(tokens)
    parser = Parser()
    if parser.parse(lines)==True:
        validation=parser.validaAST()
        if validation==True:
            checktype=parser.checktypes()
            if checktype==True:
                  Parse.execute()
            else:
                print(checktype.__repr__())
        else:
             print(validation.__repr__())
    
    else:
       print(parser.error.__repr__())

    x = 0


def test_simulation():
    print("\n\nSIMULACION:")
    time = 3  # Tiempo que demora la simulacion de una vuelta
    stop = False  # Reajustes en tiempo real
    start(time, stop)


def main():
    test_compilation()
    #test_simulation()


if __name__ == '__main__':
    main()
