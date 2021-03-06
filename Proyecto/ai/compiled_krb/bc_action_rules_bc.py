# bc_action_rules_bc.py

from pyke import contexts, pattern, bc_rule

pyke_version = '1.1.1'
compiler_version = 1

def speed_up(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('action_facts', 'speed', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules.speed_up: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def keep_speed(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('action_facts', 'speed', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules.keep_speed: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def brake(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('action_facts', 'speed', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules.brake: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def turn(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('action_facts', 'section', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules.turn: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def pits_1(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('action_facts', 'slick_tires', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules.pits_1: got unexpected plan from when clause 1"
            with engine.prove('action_facts', 'weather', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_action_rules.pits_1: got unexpected plan from when clause 2"
                rule.rule_base.num_bc_rule_successes += 1
                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def pits_2(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('action_facts', 'slick_tires', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules.pits_2: got unexpected plan from when clause 1"
            with engine.prove('action_facts', 'weather', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_action_rules.pits_2: got unexpected plan from when clause 2"
                if context.lookup_data('ans_1') != "Rainy":
                  with engine.prove('action_facts', 'humidity', context,
                                    (rule.pattern(2),)) \
                    as gen_4:
                    for x_4 in gen_4:
                      assert x_4 is None, \
                        "bc_action_rules.pits_2: got unexpected plan from when clause 4"
                      if context.lookup_data('ans_2') <= 6:
                        rule.rule_base.num_bc_rule_successes += 1
                        yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def attack_1(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('action_facts', 'section', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules.attack_1: got unexpected plan from when clause 1"
            with engine.prove('action_facts', 'nearest_forward', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_action_rules.attack_1: got unexpected plan from when clause 2"
                if context.lookup_data('ans') <= 0.5:
                  rule.rule_base.num_bc_rule_successes += 1
                  yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def attack_2(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('action_facts', 'section', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules.attack_2: got unexpected plan from when clause 1"
            with engine.prove('action_facts', 'nearest_forward', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_action_rules.attack_2: got unexpected plan from when clause 2"
                if context.lookup_data('ans') <= 1:
                  rule.rule_base.num_bc_rule_successes += 1
                  yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def defend_1(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('action_facts', 'section', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules.defend_1: got unexpected plan from when clause 1"
            with engine.prove('action_facts', 'nearest_behind', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_action_rules.defend_1: got unexpected plan from when clause 2"
                if context.lookup_data('ans') >= -0.5:
                  rule.rule_base.num_bc_rule_successes += 1
                  yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def defend_2(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(map(lambda pat, arg:
                   pat.match_pattern(context, context,
                                     arg, arg_context),
                 patterns,
                 arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('action_facts', 'section', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules.defend_2: got unexpected plan from when clause 1"
            with engine.prove('action_facts', 'nearest_behind', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_action_rules.defend_2: got unexpected plan from when clause 2"
                if context.lookup_data('ans') >= -1:
                  rule.rule_base.num_bc_rule_successes += 1
                  yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def populate(engine):
  This_rule_base = engine.get_create('bc_action_rules')
  
  bc_rule.bc_rule('speed_up', This_rule_base, 'select_action',
                  speed_up, None,
                  (pattern.pattern_literal('SpeedUp'),),
                  (),
                  (pattern.pattern_literal("Lower"),))
  
  bc_rule.bc_rule('keep_speed', This_rule_base, 'select_action',
                  keep_speed, None,
                  (pattern.pattern_literal('KeepSpeed'),),
                  (),
                  (pattern.pattern_literal("Same"),))
  
  bc_rule.bc_rule('brake', This_rule_base, 'select_action',
                  brake, None,
                  (pattern.pattern_literal('Brake'),),
                  (),
                  (pattern.pattern_literal("Higher"),))
  
  bc_rule.bc_rule('turn', This_rule_base, 'select_action',
                  turn, None,
                  (pattern.pattern_literal('Turn'),),
                  (),
                  (pattern.pattern_literal("Curve"),))
  
  bc_rule.bc_rule('pits_1', This_rule_base, 'select_action',
                  pits_1, None,
                  (pattern.pattern_literal('Pits'),),
                  (),
                  (pattern.pattern_literal(True),
                   pattern.pattern_literal("Rainy"),))
  
  bc_rule.bc_rule('pits_2', This_rule_base, 'select_action',
                  pits_2, None,
                  (pattern.pattern_literal('Pits'),),
                  (),
                  (pattern.pattern_literal(False),
                   contexts.variable('ans_1'),
                   contexts.variable('ans_2'),))
  
  bc_rule.bc_rule('attack_1', This_rule_base, 'select_action',
                  attack_1, None,
                  (pattern.pattern_literal('Attack'),),
                  (),
                  (pattern.pattern_literal("Curve"),
                   contexts.variable('ans'),))
  
  bc_rule.bc_rule('attack_2', This_rule_base, 'select_action',
                  attack_2, None,
                  (pattern.pattern_literal('Attack'),),
                  (),
                  (pattern.pattern_literal("Straight"),
                   contexts.variable('ans'),))
  
  bc_rule.bc_rule('defend_1', This_rule_base, 'select_action',
                  defend_1, None,
                  (pattern.pattern_literal('Defend'),),
                  (),
                  (pattern.pattern_literal("Curve"),
                   contexts.variable('ans'),))
  
  bc_rule.bc_rule('defend_2', This_rule_base, 'select_action',
                  defend_2, None,
                  (pattern.pattern_literal('Defend'),),
                  (),
                  (pattern.pattern_literal("Straight"),
                   contexts.variable('ans'),))


Krb_filename = '..\\bc_action_rules.krb'
Krb_lineno_map = (
    ((14, 18), (5, 5)),
    ((20, 25), (7, 7)),
    ((38, 42), (11, 11)),
    ((44, 49), (13, 13)),
    ((62, 66), (17, 17)),
    ((68, 73), (19, 19)),
    ((86, 90), (23, 23)),
    ((92, 97), (25, 25)),
    ((110, 114), (29, 29)),
    ((116, 121), (31, 31)),
    ((122, 127), (32, 32)),
    ((140, 144), (36, 36)),
    ((146, 151), (38, 38)),
    ((152, 157), (39, 39)),
    ((158, 158), (40, 40)),
    ((159, 164), (41, 41)),
    ((165, 165), (42, 42)),
    ((178, 182), (46, 46)),
    ((184, 189), (48, 48)),
    ((190, 195), (49, 49)),
    ((196, 196), (50, 50)),
    ((209, 213), (54, 54)),
    ((215, 220), (56, 56)),
    ((221, 226), (57, 57)),
    ((227, 227), (58, 58)),
    ((240, 244), (62, 62)),
    ((246, 251), (64, 64)),
    ((252, 257), (65, 65)),
    ((258, 258), (66, 66)),
    ((271, 275), (70, 70)),
    ((277, 282), (72, 72)),
    ((283, 288), (73, 73)),
    ((289, 289), (74, 74)),
)
