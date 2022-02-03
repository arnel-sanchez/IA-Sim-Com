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
        with engine.prove('action_facts', 'curve', context,
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

def pits(rule, arg_patterns, arg_context):
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
        with engine.prove('action_facts', 'tires', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules.pits: got unexpected plan from when clause 1"
            with engine.prove('action_facts', 'rainy', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_action_rules.pits: got unexpected plan from when clause 2"
                if context.lookup_data('ans_1') == context.lookup_data('ans_2'):
                  with engine.prove('action_facts', 'humidity', context,
                                    (rule.pattern(2),)) \
                    as gen_4:
                    for x_4 in gen_4:
                      assert x_4 is None, \
                        "bc_action_rules.pits: got unexpected plan from when clause 4"
                      if context.lookup_data('ans_1') == context.lookup_data('ans_3'):
                        rule.rule_base.num_bc_rule_successes += 1
                        yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def populate(engine):
  This_rule_base = engine.get_create('bc_action_rules')
  
  bc_rule.bc_rule('speed_up', This_rule_base, 'select_action',
                  speed_up, None,
                  (pattern.pattern_literal(0),),
                  (),
                  (pattern.pattern_literal(3),))
  
  bc_rule.bc_rule('keep_speed', This_rule_base, 'select_action',
                  keep_speed, None,
                  (pattern.pattern_literal(1),),
                  (),
                  (pattern.pattern_literal(2),))
  
  bc_rule.bc_rule('brake', This_rule_base, 'select_action',
                  brake, None,
                  (pattern.pattern_literal(2),),
                  (),
                  (pattern.pattern_literal(1),))
  
  bc_rule.bc_rule('turn', This_rule_base, 'select_action',
                  turn, None,
                  (pattern.pattern_literal(3),),
                  (),
                  (pattern.pattern_literal(True),))
  
  bc_rule.bc_rule('pits', This_rule_base, 'select_action',
                  pits, None,
                  (pattern.pattern_literal(6),),
                  (),
                  (contexts.variable('ans_1'),
                   contexts.variable('ans_2'),
                   contexts.variable('ans_3'),))


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
    ((128, 128), (33, 33)),
    ((129, 134), (34, 34)),
    ((135, 135), (35, 35)),
)
