# bc_moto_rules_bc.py

from pyke import contexts, pattern, bc_rule

pyke_version = '1.1.1'
compiler_version = 1

def rain_1(rule, arg_patterns, arg_context):
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
        with engine.prove('moto_facts', 'rainy', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.rain_1: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def rain_2(rule, arg_patterns, arg_context):
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
        with engine.prove('moto_facts', 'rainy', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.rain_2: got unexpected plan from when clause 1"
            with engine.prove('moto_facts', 'humidity', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_moto_rules.rain_2: got unexpected plan from when clause 2"
                rule.rule_base.num_bc_rule_successes += 1
                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def slick(rule, arg_patterns, arg_context):
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
        with engine.prove('moto_facts', 'rainy', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.slick: got unexpected plan from when clause 1"
            with engine.prove('moto_facts', 'humidity', context,
                              (rule.pattern(0),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_moto_rules.slick: got unexpected plan from when clause 2"
                rule.rule_base.num_bc_rule_successes += 1
                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def soft(rule, arg_patterns, arg_context):
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
        with engine.prove('moto_facts', 'windy', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.soft: got unexpected plan from when clause 1"
            with engine.prove('moto_facts', 'wind_direction', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_moto_rules.soft: got unexpected plan from when clause 2"
                rule.rule_base.num_bc_rule_successes += 1
                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def medium_1(rule, arg_patterns, arg_context):
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
        with engine.prove('moto_facts', 'windy', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.medium_1: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def medium_2(rule, arg_patterns, arg_context):
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
        with engine.prove('moto_facts', 'windy', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.medium_2: got unexpected plan from when clause 1"
            with engine.prove('moto_facts', 'wind_direction', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_moto_rules.medium_2: got unexpected plan from when clause 2"
                rule.rule_base.num_bc_rule_successes += 1
                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def hard(rule, arg_patterns, arg_context):
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
        with engine.prove('moto_facts', 'windy', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.hard: got unexpected plan from when clause 1"
            with engine.prove('moto_facts', 'wind_direction', context,
                              (rule.pattern(1),)) \
              as gen_2:
              for x_2 in gen_2:
                assert x_2 is None, \
                  "bc_moto_rules.hard: got unexpected plan from when clause 2"
                rule.rule_base.num_bc_rule_successes += 1
                yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def populate(engine):
  This_rule_base = engine.get_create('bc_moto_rules')
  
  bc_rule.bc_rule('rain_1', This_rule_base, 'select_type',
                  rain_1, None,
                  (pattern.pattern_literal('Rain'),),
                  (),
                  (pattern.pattern_literal(True),))
  
  bc_rule.bc_rule('rain_2', This_rule_base, 'select_type',
                  rain_2, None,
                  (pattern.pattern_literal('Rain'),),
                  (),
                  (pattern.pattern_literal(False),
                   pattern.pattern_literal(True),))
  
  bc_rule.bc_rule('slick', This_rule_base, 'select_type',
                  slick, None,
                  (pattern.pattern_literal('Slick'),),
                  (),
                  (pattern.pattern_literal(False),))
  
  bc_rule.bc_rule('soft', This_rule_base, 'select_tires',
                  soft, None,
                  (pattern.pattern_literal('Soft'),),
                  (),
                  (pattern.pattern_literal(True),
                   pattern.pattern_literal(3),))
  
  bc_rule.bc_rule('medium_1', This_rule_base, 'select_tires',
                  medium_1, None,
                  (pattern.pattern_literal('Medium'),),
                  (),
                  (pattern.pattern_literal(False),))
  
  bc_rule.bc_rule('medium_2', This_rule_base, 'select_tires',
                  medium_2, None,
                  (pattern.pattern_literal('Medium'),),
                  (),
                  (pattern.pattern_literal(True),
                   pattern.pattern_literal(2),))
  
  bc_rule.bc_rule('hard', This_rule_base, 'select_tires',
                  hard, None,
                  (pattern.pattern_literal('Hard'),),
                  (),
                  (pattern.pattern_literal(True),
                   pattern.pattern_literal(1),))


Krb_filename = '..\\bc_moto_rules.krb'
Krb_lineno_map = (
    ((14, 18), (5, 5)),
    ((20, 25), (7, 7)),
    ((38, 42), (11, 11)),
    ((44, 49), (13, 13)),
    ((50, 55), (14, 14)),
    ((68, 72), (18, 18)),
    ((74, 79), (20, 20)),
    ((80, 85), (21, 21)),
    ((98, 102), (25, 25)),
    ((104, 109), (27, 27)),
    ((110, 115), (28, 28)),
    ((128, 132), (32, 32)),
    ((134, 139), (34, 34)),
    ((152, 156), (38, 38)),
    ((158, 163), (40, 40)),
    ((164, 169), (41, 41)),
    ((182, 186), (45, 45)),
    ((188, 193), (47, 47)),
    ((194, 199), (48, 48)),
)
