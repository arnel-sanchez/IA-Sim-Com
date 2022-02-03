from os.path import exists
from shutil import rmtree
from pyke import knowledge_engine


def moto():
    engine = restart()
    #edit_moto()
    engine.activate("bc_moto_rules")
    tires = [[], []]
    with engine.prove_goal("bc_moto_rules.select_type($select)") as gen:
        for ans, plan in gen:
            tires[0].append(ans["select"])
    with engine.prove_goal("bc_moto_rules.select_tires($select)") as gen:
        for ans, plan in gen:
            tires[1].append(ans["select"])
    print("\nYou should select:")
    for i in range(len(tires[0])):
        for j in range(len(tires[1])):
            print(tires[0][i] + "_" + tires[1][j])


def restart():
    if exists("compiled_krb"):
        rmtree("compiled_krb")
    engine = knowledge_engine.engine(__file__)
    engine.reset()
    return engine


def edit_moto():
    facts = open("moto_facts.kfb", "w")
    facts.write("# moto_facts.kfb\n\n")
    facts.write("rain(True)\n")
    facts.write("humidity(False)\n")
    facts.write("windy(True)\n")
    facts.write("wind_direction(3)\n")
    facts.close()


def action():
    engine = restart()
    #edit_action()
    engine.activate("bc_action_rules")
    actions = []
    with engine.prove_goal("bc_action_rules.select_action($select)") as gen:
        for ans, plan in gen:
            actions.append(int(ans["select"]))
    return sum(actions)


def edit_action():
    facts = open("action_facts.kfb", "w")
    facts.write("# action_facts.kfb\n\n")
    facts.write("speed(3)\n")
    facts.write("curve(True)\n")
    facts.write("tires(True)\n")
    facts.write("humidity(True)\n")
    facts.close()
