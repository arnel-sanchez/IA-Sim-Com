# bc_action_rules_questions_bc.py

from pyke import contexts, pattern, bc_rule

pyke_version = '1.1.1'
compiler_version = 1

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
        with engine.prove('action_questions', 'curve', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules_questions.turn: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

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
        with engine.prove('action_questions', 'speed', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules_questions.speed_up: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def stay(rule, arg_patterns, arg_context):
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
        with engine.prove('action_questions', 'speed', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules_questions.stay: got unexpected plan from when clause 1"
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
        with engine.prove('action_questions', 'speed', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules_questions.brake: got unexpected plan from when clause 1"
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
        with engine.prove('action_questions', 'tires', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_action_rules_questions.pits: got unexpected plan from when clause 1"
            with engine.prove('action_questions', 'humidity', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_action_rules_questions.pits: got unexpected plan from when clause 2"
                if context.lookup_data('ans_1') == context.lookup_data('ans_2'):
                  rule.rule_base.num_bc_rule_successes += 1
                  yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def populate(engine):
  This_rule_base = engine.get_create('bc_action_rules_questions')
  
  bc_rule.bc_rule('turn', This_rule_base, 'select_action',
                  turn, None,
                  (pattern.pattern_literal('Turn'),),
                  (),
                  (pattern.pattern_literal(True),))
  
  bc_rule.bc_rule('speed_up', This_rule_base, 'select_action',
                  speed_up, None,
                  (pattern.pattern_literal('Speed_Up'),),
                  (),
                  (pattern.pattern_literal(3),))
  
  bc_rule.bc_rule('stay', This_rule_base, 'select_action',
                  stay, None,
                  (pattern.pattern_literal('Stay'),),
                  (),
                  (pattern.pattern_literal(2),))
  
  bc_rule.bc_rule('brake', This_rule_base, 'select_action',
                  brake, None,
                  (pattern.pattern_literal('Brake'),),
                  (),
                  (pattern.pattern_literal(1),))
  
  bc_rule.bc_rule('pits', This_rule_base, 'select_action',
                  pits, None,
                  (pattern.pattern_literal('Pits'),),
                  (),
                  (contexts.variable('ans_1'),
                   contexts.variable('ans_2'),))


Krb_filename = '..\\bc_action_rules_questions.krb'
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
)
