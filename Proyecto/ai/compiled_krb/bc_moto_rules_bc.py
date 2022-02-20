# bc_moto_rules_bc.py

from pyke import contexts, pattern, bc_rule

pyke_version = '1.1.1'
compiler_version = 1

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
        with engine.prove('moto_facts', 'weather', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.slick: got unexpected plan from when clause 1"
            if context.lookup_data('ans_1') != "Rainy":
              with engine.prove('moto_facts', 'humidity', context,
                                (rule.pattern(1),)) \
                as gen_3:
                for x_3 in gen_3:
                  assert x_3 is None, \
                    "bc_moto_rules.slick: got unexpected plan from when clause 3"
                  if context.lookup_data('ans_2') <= 6:
                    rule.rule_base.num_bc_rule_successes += 1
                    yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

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
        with engine.prove('moto_facts', 'weather', context,
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
        with engine.prove('moto_facts', 'weather', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.rain_2: got unexpected plan from when clause 1"
            if context.lookup_data('ans_1') != "Rainy":
              with engine.prove('moto_facts', 'humidity', context,
                                (rule.pattern(1),)) \
                as gen_3:
                for x_3 in gen_3:
                  assert x_3 is None, \
                    "bc_moto_rules.rain_2: got unexpected plan from when clause 3"
                  if context.lookup_data('ans_2') > 6:
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
        with engine.prove('moto_facts', 'wind_intensity', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.soft: got unexpected plan from when clause 1"
            if context.lookup_data('ans_1') > 6:
              with engine.prove('moto_facts', 'wind_direction', context,
                                (rule.pattern(1),)) \
                as gen_3:
                for x_3 in gen_3:
                  assert x_3 is None, \
                    "bc_moto_rules.soft: got unexpected plan from when clause 3"
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
        with engine.prove('moto_facts', 'wind_intensity', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.medium_1: got unexpected plan from when clause 1"
            if context.lookup_data('ans_1') <= 6:
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
        with engine.prove('moto_facts', 'wind_intensity', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.medium_2: got unexpected plan from when clause 1"
            if context.lookup_data('ans_1') > 6:
              with engine.prove('moto_facts', 'wind_direction', context,
                                (rule.pattern(1),)) \
                as gen_3:
                for x_3 in gen_3:
                  assert x_3 is None, \
                    "bc_moto_rules.medium_2: got unexpected plan from when clause 3"
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
        with engine.prove('moto_facts', 'wind_intensity', context,
                          (rule.pattern(0),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "bc_moto_rules.hard: got unexpected plan from when clause 1"
            if context.lookup_data('ans_1') > 6:
              with engine.prove('moto_facts', 'wind_direction', context,
                                (rule.pattern(1),)) \
                as gen_3:
                for x_3 in gen_3:
                  assert x_3 is None, \
                    "bc_moto_rules.hard: got unexpected plan from when clause 3"
                  rule.rule_base.num_bc_rule_successes += 1
                  yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def populate(engine):
  This_rule_base = engine.get_create('bc_moto_rules')
  
  bc_rule.bc_rule('slick', This_rule_base, 'select_type',
                  slick, None,
                  (pattern.pattern_literal('Slick'),),
                  (),
                  (contexts.variable('ans_1'),
                   contexts.variable('ans_2'),))
  
  bc_rule.bc_rule('rain_1', This_rule_base, 'select_type',
                  rain_1, None,
                  (pattern.pattern_literal('Rain'),),
                  (),
                  (pattern.pattern_literal("Rainy"),))
  
  bc_rule.bc_rule('rain_2', This_rule_base, 'select_type',
                  rain_2, None,
                  (pattern.pattern_literal('Rain'),),
                  (),
                  (contexts.variable('ans_1'),
                   contexts.variable('ans_2'),))
  
  bc_rule.bc_rule('soft', This_rule_base, 'select_tires',
                  soft, None,
                  (pattern.pattern_literal('Soft'),),
                  (),
                  (contexts.variable('ans_1'),
                   pattern.pattern_literal(3),))
  
  bc_rule.bc_rule('medium_1', This_rule_base, 'select_tires',
                  medium_1, None,
                  (pattern.pattern_literal('Medium'),),
                  (),
                  (contexts.variable('ans_1'),))
  
  bc_rule.bc_rule('medium_2', This_rule_base, 'select_tires',
                  medium_2, None,
                  (pattern.pattern_literal('Medium'),),
                  (),
                  (contexts.variable('ans_1'),
                   pattern.pattern_literal(2),))
  
  bc_rule.bc_rule('hard', This_rule_base, 'select_tires',
                  hard, None,
                  (pattern.pattern_literal('Hard'),),
                  (),
                  (contexts.variable('ans_1'),
                   pattern.pattern_literal(1),))


Krb_filename = '..\\bc_moto_rules.krb'
Krb_lineno_map = (
    ((14, 18), (5, 5)),
    ((20, 25), (7, 7)),
    ((26, 26), (8, 8)),
    ((27, 32), (9, 9)),
    ((33, 33), (10, 10)),
    ((46, 50), (14, 14)),
    ((52, 57), (16, 16)),
    ((70, 74), (20, 20)),
    ((76, 81), (22, 22)),
    ((82, 82), (23, 23)),
    ((83, 88), (24, 24)),
    ((89, 89), (25, 25)),
    ((102, 106), (29, 29)),
    ((108, 113), (31, 31)),
    ((114, 114), (32, 32)),
    ((115, 120), (33, 33)),
    ((133, 137), (37, 37)),
    ((139, 144), (39, 39)),
    ((145, 145), (40, 40)),
    ((158, 162), (44, 44)),
    ((164, 169), (46, 46)),
    ((170, 170), (47, 47)),
    ((171, 176), (48, 48)),
    ((189, 193), (52, 52)),
    ((195, 200), (54, 54)),
    ((201, 201), (55, 55)),
    ((202, 207), (56, 56)),
)
