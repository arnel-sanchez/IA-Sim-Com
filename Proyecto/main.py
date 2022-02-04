from compilation.tokenizer import Tokenizer
from compilation.utils import split_lines
from compilation.parser import *
from simulation.bike import Bike, Tires
from simulation.environment import Environment
from simulation.rider import Rider
from simulation.simulator import Simulator
from simulation.race import Race
from simulation.agent import Agent

from simulation.SetOffClasses.Bikes.ducati import Ducati
from simulation.SetOffClasses.Riders.pecco_bagnaia import Bagnaia
from simulation.SetOffClasses.Bikes.yamaha import Yamaha
from simulation.SetOffClasses.Riders.fabio_quartararo import Quartararo
from simulation.SetOffClasses.Bikes.aprilia import Aprilia
from simulation.SetOffClasses.Riders.aleix_espargaro import Espargaro
from simulation.SetOffClasses.Bikes.honda import Honda
from simulation.SetOffClasses.Riders.marc_marquez import Marquez
from simulation.SetOffClasses.Bikes.suzuki import Suzuki
from simulation.SetOffClasses.Riders.joan_mir import Mir
from simulation.SetOffClasses.Bikes.ktm import KTM
from simulation.SetOffClasses.Riders.brad_binder import Binder

from simulation.SetOffClasses.Tracks.misano import Misano
from simulation.track import Track


def compilation():
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
                  
                  exe=parser.execute()
                  if isinstance(exe, RuntimeError):
                     print(checktype.__repr__())
                  else:
                      return parser.Riders,parser.Motorcicles      
            else:
                print(checktype.__repr__())
                return False
        else:
             print(validation.__repr__())
             return False
    else:
       print(parser.error.__repr__())
       return False
    x = 0


def simulation():
    print("\n\nSIMULACION:")
    t = Misano()
    environment = Environment(Track(t.name, t.length, t.sections))

    agents = []
    b = Bagnaia()
    d = Ducati()
    rider = Rider(b.name, b.cornering, b.step_by_line)
    bike = Bike(d.brand, d.max_speed, d.weight)
    if False:
        bike.select_configuration(environment)
    else:
        print("Aquí se llama al nodo")
    agents.append(Agent(rider, bike, False, False, False, None ))
    '''
    m = Mir()
    s = Suzuki()
    agent.append(Agent(Rider(m.name, m.cornering, m.step_by_line), Bike(s.brand, s.max_speed, s.weight)))
    e = Espargaro()
    a = Aprilia()
    agent.append(Agent(Rider(e.name, e.cornering, e.step_by_line), Bike(a.brand, a.max_speed, a.weight)))
    ma = Marquez()
    h = Honda()
    agent.append(Agent(Rider(ma.name, ma.cornering, ma.step_by_line), Bike(h.brand, h.max_speed, h.weight)))
    q = Quartararo()
    y = Yamaha()
    agent.append(Agent(Rider(q.name, q.cornering, q.step_by_line), Bike(y.brand, y.max_speed, y.weight)))
    bi = Binder()
    k = KTM()
    agent.append(Agent(Rider(bi.name, bi.cornering, bi.step_by_line), Bike(k.brand, k.max_speed, k.weight)))
    '''

    race = Race(environment, agents, 5)

    time = 1  # Tiempo que demora la simulacion de una vuelta
    stop = False  # Reajustes en tiempo real
    s = Simulator()
    s.start(time, stop, race)


def main():

    resultComp=compilation()
    if resultComp!=False:
      simulation(resultComp)




if __name__ == '__main__':
    main()
