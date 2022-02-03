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
           [1643916506.7812662, 'action_facts.fbc'],
         ('', '', 'action_questions.kqb'):
           [1643916506.8044071, 'action_questions.qbc'],
         ('', '', 'bc_action_rules.krb'):
           [1643916506.8293414, 'bc_action_rules_bc.py'],
         ('', '', 'bc_action_rules_questions.krb'):
           [1643916506.8492882, 'bc_action_rules_questions_bc.py'],
         ('', '', 'bc_moto_rules.krb'):
           [1643916506.877177, 'bc_moto_rules_bc.py'],
         ('', '', 'bc_moto_rules_questions.krb'):
           [1643916506.9041455, 'bc_moto_rules_questions_bc.py'],
         ('', '', 'moto_facts.kfb'):
           [1643916506.9051018, 'moto_facts.fbc'],
         ('', '', 'moto_questions.kqb'):
           [1643916506.9080966, 'moto_questions.qbc'],
         ('', '', 'pilot_questions.kqb'):
           [1643916506.9100883, 'pilot_questions.qbc'],
        },
        compiler_version)

