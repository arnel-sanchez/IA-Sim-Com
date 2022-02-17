from subprocess import run, PIPE, STDOUT
from sys import path
from os.path import exists
from shutil import rmtree
from pyke import knowledge_engine

from random import uniform


def call_ai(script: str):
    try:
        ans = call_subprocess("python3 ", script)
    except Exception:
        ans = call_subprocess("python ", script)
    return ans


def call_subprocess(python: str, script: str):
    ans = run(python + "./ai/" + script, shell=True, stdout=PIPE, stderr=STDOUT)
    if ans.returncode != 0:
        raise Exception
    ans = ans.stdout.decode("utf-8")
    ans = ans.replace("\n", "").replace("\r", "").split(".py")
    return int(ans[-1])


def edit_moto(environment):
    weather = environment.weather
    front = 0
    back = 0
    side = 0
    for section in environment.track.sections:
        if weather.is_front_wind(section.orientation):
            front += 1
        elif weather.is_back_wind(section.orientation):
            back += 1
        else:
            side += 1
    if front > back and front > side:
        direction = 1
    elif back > front and back > side:
        direction = 3
    else:
        direction = 2
    facts = open(path[0] + "/ai/moto_facts.kfb", "w+")
    facts.write("# moto_facts.kfb\n\n")
    facts.write("weather({})\n".format(weather.weather_status.name))
    facts.write("humidity({})\n".format(weather.humidity))
    facts.write("wind_intensity({})\n".format(weather.wind_intensity))
    facts.write("wind_direction({})\n".format(direction))
    facts.close()


def call_moto():
    engine = restart("bc_moto_rules")
    tires = [[], []]
    with engine.prove_goal("bc_moto_rules.select_type($select)") as gen:
        for ans, plan in gen:
            tires[0].append(ans["select"])
    with engine.prove_goal("bc_moto_rules.select_tires($select)") as gen:
        for ans, plan in gen:
            tires[1].append(ans["select"])
    for i in range(len(tires[0])):
        for j in range(len(tires[1])):
            comb = tires[0][i] + tires[1][j]
            print(comb if comb < 5 else 4)


def restart(rules: str):
    if exists(path[0] + "/compiled_krb"):
        rmtree(path[0] + "/compiled_krb")
    if exists(path[0] + "/ai/compiled_krb"):
        rmtree(path[0] + "/ai/compiled_krb")
    engine = knowledge_engine.engine(__file__)
    engine.reset()
    engine.activate(rules)
    return engine


def edit_action(race, agent):
    speed = agent.speed
    bike = agent.bike
    section_max_speed = agent.section.max_speed
    if speed > bike.max_speed or speed > section_max_speed:
        speed_cmp = 1
    elif speed < bike.max_speed and speed < section_max_speed:
        speed_cmp = 3
    else:
        speed_cmp = 2
    section_type = agent.section.type.name
    weather = race.environment.weather
    nearest_forward, nearest_behind = nearest(race, agent)
    facts = open(path[0] + "/ai/action_facts.kfb", "w")
    facts.write("# action_facts.kfb\n\n")
    facts.write("speed({})\n".format(speed_cmp))
    facts.write("section({})\n".format(section_type))
    facts.write("slick_tires({})\n".format(True if bike.tires.name.__contains__("Slick") else False))
    facts.write("rainy({})\n".format(True if weather.weather_status.name == "Rainy" else False))
    facts.write("high_humidity({})\n".format(True if weather.humidity > 6 else False))
    facts.write("nearest_forward({})\n".format(nearest_forward))
    facts.write("nearest_behind({})\n".format(nearest_behind))
    facts.close()


def nearest(race, agent):
    nearest_forward = 60
    nearest_behind = 60
    for i in range(len(race.agents)):
        if agent == race.agents[i]:
            if i > 0:
                nearest_forward = how_close(agent, race.agents[i - 1])
            elif i < len(race.agents) - 1:
                nearest_behind = how_close(agent, race.agents[i + 1])
    return nearest_forward, nearest_behind


def how_close(agent_1, agent_2):
    if agent_1.time_track == 0 or agent_2.time_track == 0 or agent_1.section != agent_2.section:
        return 60
    return abs(agent_1.time_track - agent_2.time_track)


def call_action():
    engine = restart("bc_action_rules")
    actions = []
    with engine.prove_goal("bc_action_rules.select_action($select)") as gen:
        for ans, plan in gen:
            actions.append(int(ans["select"]))
    action = 0
    for a in actions:
        if a > 11 and (action > 11 or random(1) < 0.5):
            continue
        action += a
    print(action)


def acceleration(race, agent, action, max_acceleration):
    if action.name.__contains__("KeepSpeed"):
        return 0
    weather = race.environment.weather
    weather_status = [weather.weather_status == 1,
                      3 < weather.humidity < 7,
                      3 < weather.temperature < 7,
                      3 < weather.visibility < 7,
                      3 < weather.wind_intensity < 7]
    rider = agent.rider
    aggressiveness = rider.aggressiveness
    for w in weather_status:
        if not w:
            max_acceleration -= random(0.1)
        else:
            aggressiveness += random(0.01)
    section = agent.section
    bike = agent.bike
    if section.type.name == "Straight":
        if bike.brakes < 8 and bike.chassis_stiffness < 8:
            max_acceleration -= random(0.3)
        else:
            aggressiveness += random(0.03)
        if rider.step_by_line < 8:
            max_acceleration -= random(0.6)
        else:
            aggressiveness += random(0.06)
    else:
        if bike.brakes != 5 and bike.chassis_stiffness != 5:
            max_acceleration -= random(0.3)
        else:
            aggressiveness += random(0.03)
        if rider.cornering < 8:
            max_acceleration -= random(0.6)
        else:
            aggressiveness += random(0.06)
    if action.name.__contains__("Attack") or action.name.__contains__("Defend"):
        aggressiveness += random(0.1)
    if max_acceleration < 0 and action.name.__contains__("SpeedUp"):
        max_acceleration = (- max_acceleration) / 10
    if len(race.agents) > 1 and aggressiveness > random(1):
        max_acceleration += random(0.01)
    return max_acceleration


def random(n: float):
    return uniform(0, n)
