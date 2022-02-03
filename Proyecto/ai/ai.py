from os.path import exists
from shutil import rmtree
from pyke import knowledge_engine


def moto():
    # edit_moto()
    engine = restart()
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
    if exists("ai/compiled_krb"):
        rmtree("ai/compiled_krb")
    engine = knowledge_engine.engine(__file__)
    engine.reset()
    return engine


def edit_moto(self):
    facts = open("moto_facts.kfb", "w")
    facts.write("# moto_facts.kfb\n\n")
    facts.write("rain(True)\n")
    facts.write("humidity(False)\n")
    facts.write("windy(True)\n")
    facts.write("wind_direction(3)\n")
    facts.close()


def action():#section_type, tires, weather, humidity):
    #edit_action(section_type, tires, weather, humidity)
    engine = restart()
    #engine.assert_("action_facts", "speed", ("2", ))
    engine.activate("bc_action_rules")
    #x = engine.prove_1_goal("bc_action_rules.select_action($select)")
    actions = []
    with engine.prove_goal("bc_action_rules.select_action($select)") as gen:
        for ans, plan in gen:
            actions.append(int(ans["select"]))
    print(sum(actions))#return sum(actions)


def edit_action(section_type, tires, weather, humidity):
    facts = open("ai/action_facts.kfb", "w")
    facts.write("# action_facts.kfb\n\n")
    facts.write("speed(3)\n")
    facts.write("curve({})\n".format(True if section_type == "Curve" else False))
    facts.write("tires({})\n".format(True if tires.__contains__("Slick") else False))
    facts.write("rainy({})\n".format(True if weather.__contains__("Rainy") else False))
    facts.write("humidity({})\n".format(True if humidity > 6 else False))
    facts.close()

action()
