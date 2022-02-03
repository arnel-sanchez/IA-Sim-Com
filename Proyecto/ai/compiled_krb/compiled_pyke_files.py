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
           [1643931439.5668788, 'action_facts.fbc'],
         ('', '', 'action_questions.kqb'):
           [1643931439.5838542, 'action_questions.qbc'],
         ('', '', 'bc_action_rules.krb'):
           [1643931439.6103027, 'bc_action_rules_bc.py'],
         ('', '', 'bc_action_rules_questions.krb'):
           [1643931439.6312456, 'bc_action_rules_questions_bc.py'],
         ('', '', 'bc_moto_rules.krb'):
           [1643931439.6581726, 'bc_moto_rules_bc.py'],
         ('', '', 'bc_moto_rules_questions.krb'):
           [1643931439.6841052, 'bc_moto_rules_questions_bc.py'],
         ('', '', 'moto_facts.kfb'):
           [1643931439.685134, 'moto_facts.fbc'],
         ('', '', 'moto_questions.kqb'):
           [1643931439.6870959, 'moto_questions.qbc'],
         ('', '', 'pilot_questions.kqb'):
           [1643931439.6890907, 'pilot_questions.qbc'],
        },
        compiler_version)

