from sys import path

from compilation.tokenizer import Tokenizer
from compilation.utils import split_lines
from compilation.parser import Parser

from simulation.environment import Environment
from simulation.track import Track
from simulation.rider import Rider
from simulation.bike import Bike
from simulation.agent import Agent
from simulation.race import Race
from simulation.simulator import Simulator

from simulation.set_off_classes.tracks.misano import Misano
from simulation.set_off_classes.bikes.ducati import Ducati
from simulation.set_off_classes.riders.pecco_bagnaia import Bagnaia
from simulation.set_off_classes.bikes.yamaha import Yamaha
from simulation.set_off_classes.riders.fabio_quartararo import Quartararo
from simulation.set_off_classes.bikes.aprilia import Aprilia
from simulation.set_off_classes.riders.aleix_espargaro import Espargaro
from simulation.set_off_classes.bikes.honda import Honda
from simulation.set_off_classes.riders.marc_marquez import Marquez
from simulation.set_off_classes.bikes.suzuki import Suzuki
from simulation.set_off_classes.riders.joan_mir import Mir
from simulation.set_off_classes.bikes.ktm import KTM
from simulation.set_off_classes.riders.brad_binder import Binder


def compilation(case: str):
    print("\nCOMPILACION:\n")
    tokenizer = Tokenizer()
    file = "console"
    if case is None:
        text = open(path[0] + "/codes/Prueba19.pys").read()
    else:
        text = open(path[0] + "/codes/" + case).read()
    tokens, error = tokenizer.tokenize(file, text)
    if error is not None:
        print(error)
        return False
    lines = split_lines(tokens)
    parser = Parser()
    if parser.parse(lines) == True:
        validation = parser.validaAST()
        if validation == True:
            checktype = parser.checktypes()
            if checktype == True:
                exe = parser.execute()
                if isinstance(exe, RuntimeError):
                    print(exe.__repr__())
                else:
                    parser.LoadRidersAndBikes()
                    return parser.Riders, parser.Bikes
            else:
                print(checktype.__repr__())
                return False
        else:
            print(validation.__repr__())
            return False
    else:
        print(parser.error.__repr__())
        return False


def simulation(agents_lists):
    print("\n\nSIMULACION:")
    track = Misano()
    environment = Environment(Track(track.name, track.length, track.sections))
    agents = []
    if len(agents_lists[0]) >= 2:
        for i in range(len(agents_lists[0])):
            rider = Rider(agents_lists[0][i].id, agents_lists[0][i].varsforRiders[3][2],
                          agents_lists[0][i].varsforRiders[4][2])
            if len(agents_lists[1]) > i:
                bike = Bike(agents_lists[1][i].varsforBikes[0][2], "test", agents_lists[1][i].varsforBikes[1][2],
                            agents_lists[1][i].varsforBikes[2][2], agents_lists[1][i],
                            agents_lists[1][i].varsforBikes[4][2], agents_lists[1][i].varsforBikes[5][2])
                if len(agents_lists[1][i].funciones) == 0:
                    flag_configuration = False
                else:
                    flag_configuration = True
            else:
                d = Ducati()
                bike = Bike(d.brand, d.max_speed, d.weight, None)
                flag_configuration = False
            if len(agents_lists[0][i].funciones) == 0:
                flag_acceleration = False
                flag_action = False
            elif len(agents_lists[0][i].funciones) == 1 and agents_lists[0][i].funciones[0] == "select_action":
                flag_acceleration = False
                flag_action = True
            elif len(agents_lists[0][i].funciones) == 1 and agents_lists[0][i].funciones[0] == "select_acceleration":
                flag_acceleration = True
                flag_action = False
            else:
                flag_acceleration = True
                flag_action = True
            agents.append(Agent(rider, bike, flag_configuration, flag_action, flag_acceleration, agents_lists[0][i]))
    else:
        if len(agents_lists[0]) == 1:
            rider = Rider(agents_lists[0][0].id, agents_lists[0][0].varsforRiders[3][2],
                          agents_lists[0][0].varsforRiders[4][2])
            if len(agents_lists[1]) >= 1:
                bike = Bike(agents_lists[1][0].varsforBikes[0][2], "test", agents_lists[1][0].varsforBikes[1][2],
                            agents_lists[1][0].varsforBikes[2][2], agents_lists[1][0],
                            agents_lists[1][0].varsforBikes[4][2], agents_lists[1][0].varsforBikes[5][2])
                if len(agents_lists[1][0].funciones) == 0:
                    flag_configuration = False
                else:
                    flag_configuration = True
            else:
                d = Ducati()
                bike = Bike(d.brand, d.model, d.max_speed, d.weight, None)
                flag_configuration = False
            if len(agents_lists[0][0].funciones) == 0:
                flag_acceleration = False
                flag_action = False
            elif len(agents_lists[0][0].funciones) == 1 and agents_lists[0][0].funciones[0] == "select_action":
                flag_acceleration = False
                flag_action = True
            elif len(agents_lists[0][0].funciones) == 1 and agents_lists[0][0].funciones[0] == "select_acceleration":
                flag_acceleration = True
                flag_action = False
            else:
                flag_acceleration = True
                flag_action = True
            agents.append(Agent(rider, bike, flag_configuration, flag_action, flag_acceleration, agents_lists[0][0]))
        
        b = Bagnaia()
        d = Ducati()
        rider = Rider(b.name, b.cornering, b.step_by_line)
        bike = Bike(d.brand, d.model, d.max_speed, d.weight, None)
        agents.append(Agent(rider, bike, False, False, False))
        
        m = Mir()
        s = Suzuki()
        rider = Rider(m.name, m.cornering, m.step_by_line)
        bike = Bike(s.brand, s.model, s.max_speed, s.weight, None)
        agents.append(Agent(rider, bike, False, False, False))
        
        e = Espargaro()
        a = Aprilia()
        rider = Rider(e.name, e.cornering, e.step_by_line)
        bike = Bike(a.brand, a.model, a.max_speed, a.weight, None)
        agents.append(Agent(rider, bike, False, False, False))

        ma = Marquez()
        h = Honda()
        rider = Rider(ma.name, ma.cornering, ma.step_by_line)
        bike = Bike(h.brand, h.model, h.max_speed, h.weight, None)
        agents.append(Agent(rider, bike, False, False, False))

        q = Quartararo()
        y = Yamaha()
        rider = Rider(q.name, q.cornering, q.step_by_line)
        bike = Bike(y.brand, y.model, y.max_speed, y.weight, None)
        agents.append(Agent(rider, bike, False, False, False))

        bi = Binder()
        k = KTM()
        rider = Rider(bi.name, bi.cornering, bi.step_by_line)
        bike = Bike(k.brand, k.model, k.max_speed, k.weight, None)
        agents.append(Agent(rider, bike, False, False, False))
        
    race = Race(environment, agents, 5)
    s = Simulator()
    s.start(race)


def main(case: str = None):
    comp = compilation(case)
    if comp:
        print("Ok")
        simulation(comp)


if __name__ == '__main__':
    main(None)
