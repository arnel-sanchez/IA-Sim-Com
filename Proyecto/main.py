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
    file, text = "console", ""
    tokens, error = tokenizer.tokenize(file, text)
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
                      parser.LoadRidersAndBikes()
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


def simulation(listsOfAgents):
    print("\n\nSIMULACION:")
    t = Misano()
    environment = Environment(Track(t.name, t.length, t.sections))
    agents = []
    if len(listsOfAgents[0]) >=2:
        for i in len(listsOfAgents[0]):
            rider = Rider(listsOfAgents[0][i].id, listsOfAgents[0][i].cornering, listsOfAgents[0][i].step_by_line)
            if listsOfAgents[1][i] != None:
                bike = Bike(listsOfAgents[1][i].brand, listsOfAgents[1][i].max_speed, listsOfAgents[1][i].weight)
                if len(listsOfAgents[1][i].functionsOfMotorcicles) == 0:
                    flag = False
                else:
                    flag = True
            else:
                d = Ducati()
                bike = Bike(d.brand, d.max_speed, d.weight)
                flag = False

            if flag == False:
                bike.select_configuration(environment)
            else:
                print("Aquí se llama al nodo")
            agents.append(Agent(rider, bike, flag, False, False, None ))
    else:
        if len(listsOfAgents[0]) == 1:
            rider = Rider(listsOfAgents[0][0].name, listsOfAgents[0][0].cornering, blistsOfAgents[0][0].step_by_line)
            if listsOfAgents[1] != None:
                bike = Bike(listsOfAgents[1][0].brand, listsOfAgents[1][0].max_speed, listsOfAgents[1][0].weight)
                if len(listsOfAgents[1][i].functionsOfMotorcicles) == 0:
                    flag = False
                else:
                    flag = True
            else:
                d = Ducati()
                bike = Bike(d.brand, d.max_speed, d.weight)
                flag = False

            if flag == False:
                bike.select_configuration(environment)
            else:
                print("Aquí se llama al nodo")
            agents.append(Agent(rider, bike, flag, False, False, None ))
        
        b = Bagnaia()
        d = Ducati()
        rider = Rider(b.name, b.cornering, b.step_by_line)
        bike = Bike(d.brand, d.max_speed, d.weight)
        bike.select_configuration(environment)
        agents.append(Agent(rider, bike, False, False, False, None ))
        
        m = Mir()
        s = Suzuki()
        rider = Rider(m.name, m.cornering, m.step_by_line)
        bike = Bike(s.brand, s.max_speed, s.weight)
        bike.select_configuration(environment)
        agents.append(Agent(rider, bike, False, False, False, None ))
        
        e = Espargaro()
        a = Aprilia()
        rider = Rider(e.name, e.cornering, e.step_by_line)
        bike = Bike(a.brand, a.max_speed, a.weight)
        bike.select_configuration(environment)
        agents.append(Agent(rider, bike, False, False, False, None ))

        ma = Marquez()
        h = Honda()
        rider = Rider(ma.name, ma.cornering, ma.step_by_line)
        bike = Bike(h.brand, h.max_speed, h.weight)
        bike.select_configuration(environment)
        agents.append(Agent(rider, bike, False, False, False, None ))

        q = Quartararo()
        y = Yamaha()
        rider = Rider(q.name, q.cornering, q.step_by_line)
        bike = Bike(y.brand, y.max_speed, y.weight)
        bike.select_configuration(environment)
        agents.append(Agent(rider, bike, False, False, False, None ))

        bi = Binder()
        k = KTM()
        rider = Rider(bi.name, bi.cornering, bi.step_by_line)
        bike = Bike(k.brand, k.max_speed, k.weight)
        bike.select_configuration(environment)
        agents.append(Agent(rider, bike, False, False, False, None ))

    race = Race(environment, agents, 5)

    time = 0.5  # Tiempo que demora la simulacion de una vuelta
    stop = False  # Reajustes en tiempo real
    s = Simulator()
    s.start(time, stop, race)


def main():

    resultComp=compilation()
    if resultComp!=False:
      simulation(resultComp)




if __name__ == '__main__':
    main()
