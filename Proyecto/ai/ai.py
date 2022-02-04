import subprocess
from os.path import exists
from shutil import rmtree
from pyke import knowledge_engine


def call_ai(script: str):
    ans = subprocess.run(script, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return int(ans.stdout.decode("utf-8")[-3])


def edit_moto(weather):
    facts = open("ai/moto_facts.kfb", "w")
    facts.write("# moto_facts.kfb\n\n")
    facts.write("rainy({})\n".format(True if weather.weather_status.name.__contains__("Rainy") else False))
    facts.write("humidity({})\n".format(True if weather.humidity > 6 else False))
    facts.write("windy({})\n".format(True if weather.wind_intensity > 6 else False))
    facts.write("wind_direction(3)\n")
    facts.close()


def moto():
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
    if exists("compiled_krb"):
        rmtree("compiled_krb")
    if exists("ai/compiled_krb"):
        rmtree("ai/compiled_krb")
    engine = knowledge_engine.engine(__file__)
    engine.reset()
    engine.activate(rules)
    return engine


def edit_action(speed, bike_max_speed, section_max_speed, section_type, tires, weather):
    facts = open("ai/action_facts.kfb", "w")
    facts.write("# action_facts.kfb\n\n")
    if speed > bike_max_speed or speed > section_max_speed:
        speed_cmp = 1
    elif speed < bike_max_speed and speed < section_max_speed:
        speed_cmp = 3
    else:
        speed_cmp = 2
    facts.write("speed({})\n".format(speed_cmp))
    facts.write("curve({})\n".format(True if section_type == "Curve" else False))
    facts.write("tires({})\n".format(True if tires.__contains__("Slick") else False))
    facts.write("rainy({})\n".format(True if weather.weather_status.name.__contains__("Rainy") else False))
    facts.write("humidity({})\n".format(True if weather.humidity > 6 else False))
    facts.close()


def action():
    engine = restart("bc_action_rules")
    actions = []
    with engine.prove_goal("bc_action_rules.select_action($select)") as gen:
        for ans, plan in gen:
            actions.append(int(ans["select"]))
    print(sum(actions))