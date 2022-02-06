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
import sys

def compilation():
    print("\nCOMPILACION:\n")
    tokenizer = Tokenizer()
    # file, text = "console", "rider Arnel{method void select_aceleration(){if(time_lap<19.5){aceleration+=30.3;}}}bike Palmiche{method void select_configuration(){tires=7;}}"
    file = "console"
    text = open(sys.path[0]+"/codes/PruebaTipos.pys").read()
    tokens, error = tokenizer.tokenize(file, text)
    if error is not None:
        print(error)
        return False
    lines = split_lines(tokens)
    parser = Parser()
    if parser.parse(lines)==True:
        validation=parser.validaAST()
        if validation==True:
            checktype=parser.checktypes()
            if checktype==True:
                  
                  exe=parser.execute()
                  if isinstance(exe, RuntimeError):
                     print(exe.__repr__())
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
        for i in range(len(listsOfAgents[0])):
            rider = Rider(listsOfAgents[0][i].id, listsOfAgents[0][i].varsforRiders[3][2], listsOfAgents[0][i].varsforRiders[4][2])
            if len(listsOfAgents[1][i]) >=1:
                bike = Bike(listsOfAgents[1][i].varsforBikes[0][2], listsOfAgents[1][i].varsforBikes[1][2], listsOfAgents[1][i].varsforBikes[2][2], listsOfAgents[1][i].varsforBikes[3][2], listsOfAgents[1][i].varsforBikes[4][2],listsOfAgents[1][i])
                if len(listsOfAgents[1][i].funciones) == 0:
                    flag_configuration = False
                else:
                    flag_configuration = True
                
                if len(listsOfAgents[0][i].funciones) == 0:
                    flag_aceleration = False
                    flag_action = False
                elif len(listsOfAgents[0][i].funciones) == 1 and listsOfAgents[0][i].funciones[0] == "select_action":
                    flag_aceleration = False
                    flag_action = True
                elif len(listsOfAgents[0][i].funciones) == 1 and listsOfAgents[0][i].funciones[0] == "select_aceleration":
                    flag_aceleration = True
                    flag_action = False
                else:
                    flag_aceleration = True
                    flag_action = True
            else:
                d = Ducati()
                bike = Bike(d.brand, d.max_speed, d.weight,None)
                flag = False

                if len(listsOfAgents[0][i].funciones) == 0:
                    flag_aceleration = False
                    flag_action = False
                elif len(listsOfAgents[0][i].funciones) == 1 and listsOfAgents[0][i].funciones[0] == "select_action":
                    flag_aceleration = False
                    flag_action = True
                elif len(listsOfAgents[0][i].funciones) == 1 and listsOfAgents[0][i].funciones[0] == "select_aceleration":
                    flag_aceleration = True
                    flag_action = False
                else:
                    flag_aceleration = True
                    flag_action = True
            agents.append(Agent(rider, bike, flag_configuration, flag_action, flag_aceleration, listsOfAgents[0][i] ))
    else:
        if len(listsOfAgents[0]) == 1:
            rider = Rider(listsOfAgents[0][0].id, listsOfAgents[0][0].varsforRiders[3][2], listsOfAgents[0][0].varsforRiders[4][2])
            if len(listsOfAgents[1]) >= 1:
                bike = Bike(listsOfAgents[1][0].varsforBikes[0][2], listsOfAgents[1][0].varsforBikes[1][2], listsOfAgents[1][0].varsforBikes[2][2], listsOfAgents[1][0], listsOfAgents[1][0].varsforBikes[3][2], listsOfAgents[1][0].varsforBikes[4][2])
                if len(listsOfAgents[1][0].funciones) == 0:
                    flag_configuration = False
                else:
                    flag_configuration = True
                
                if len(listsOfAgents[0][0].funciones) == 0:
                    flag_aceleration = False
                    flag_action = False
                elif len(listsOfAgents[0][0].funciones) == 1 and listsOfAgents[0][0].funciones[0] == "select_action":
                    flag_aceleration = False
                    flag_action = True
                elif len(listsOfAgents[0][0].funciones) == 1 and listsOfAgents[0][0].funciones[0] == "select_aceleration":
                    flag_aceleration = True
                    flag_action = False
                else:
                    flag_aceleration = True
                    flag_action = True
            else:
                d = Ducati()
                bike = Bike(d.brand, d.max_speed, d.weight, None)
                flag_configuration = False

                if len(listsOfAgents[0][0].funciones) == 0:
                    flag_aceleration = False
                    flag_action = False
                elif len(listsOfAgents[0][0].funciones) == 1 and listsOfAgents[0][0].funciones[0] == "select_action":
                    flag_aceleration = False
                    flag_action = True
                elif len(listsOfAgents[0][0].funciones) == 1 and listsOfAgents[0][0].funciones[0] == "select_aceleration":
                    flag_aceleration = True
                    flag_action = False
                else:
                    flag_aceleration = True
                    flag_action = True
            agents.append(Agent(rider, bike, flag_configuration, flag_action, flag_aceleration, listsOfAgents[0][0] ))
        
        b = Bagnaia()
        d = Ducati()
        rider = Rider(b.name, b.cornering, b.step_by_line)
        bike = Bike(d.brand, d.max_speed, d.weight, None)
        agents.append(Agent(rider, bike, False, False, False, None ))
        
        m = Mir()
        s = Suzuki()
        rider = Rider(m.name, m.cornering, m.step_by_line)
        bike = Bike(s.brand, s.max_speed, s.weight, None)
        agents.append(Agent(rider, bike, False, False, False, None ))
        
        e = Espargaro()
        a = Aprilia()
        rider = Rider(e.name, e.cornering, e.step_by_line)
        bike = Bike(a.brand, a.max_speed, a.weight, None)
        agents.append(Agent(rider, bike, False, False, False, None ))

        ma = Marquez()
        h = Honda()
        rider = Rider(ma.name, ma.cornering, ma.step_by_line)
        bike = Bike(h.brand, h.max_speed, h.weight, None)
        agents.append(Agent(rider, bike, False, False, False, None ))

        q = Quartararo()
        y = Yamaha()
        rider = Rider(q.name, q.cornering, q.step_by_line)
        bike = Bike(y.brand, y.max_speed, y.weight, None)
        agents.append(Agent(rider, bike, False, False, False, None ))

        bi = Binder()
        k = KTM()
        rider = Rider(bi.name, bi.cornering, bi.step_by_line)
        bike = Bike(k.brand, k.max_speed, k.weight, None)
        agents.append(Agent(rider, bike, False, False, False, None ))

    race = Race(environment, agents, 5)
    s = Simulator()
    s.start(race)


def main():

    resultComp=compilation()
    if resultComp!=False:
      simulation(resultComp)

if __name__ == '__main__':
    main()
