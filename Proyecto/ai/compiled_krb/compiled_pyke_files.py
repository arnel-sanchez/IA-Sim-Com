# compiled_pyke_files.py

from pyke import target_pkg

pyke_version = '1.1.1'
compiler_version = 1
target_pkg_version = 1

try:
    loader = __loader__
except NameError:
    loader = None

def get_target_pkg():
    return target_pkg.target_pkg(__name__, __file__, pyke_version, loader, {
         ('', '', 'action_facts.kfb'):
           [1643994795.0378978, 'action_facts.fbc'],
         ('', '', 'action_questions.kqb'):
           [1643994795.0648818, 'action_questions.qbc'],
         ('', '', 'bc_action_rules.krb'):
           [1643994795.0878665, 'bc_action_rules_bc.py'],
         ('', '', 'bc_action_rules_questions.krb'):
           [1643994795.1078541, 'bc_action_rules_questions_bc.py'],
         ('', '', 'bc_moto_rules.krb'):
           [1643994795.1358364, 'bc_moto_rules_bc.py'],
         ('', '', 'bc_moto_rules_questions.krb'):
           [1643994795.1558244, 'bc_moto_rules_questions_bc.py'],
         ('', '', 'moto_facts.kfb'):
           [1643994795.1608222, 'moto_facts.fbc'],
         ('', '', 'moto_questions.kqb'):
           [1643994795.166818, 'moto_questions.qbc'],
        },
        compiler_version)

