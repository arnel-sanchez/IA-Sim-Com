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
           [1643932984.5862603, 'action_facts.fbc'],
         ('', '', 'action_questions.kqb'):
           [1643932984.6036215, 'action_questions.qbc'],
         ('', '', 'bc_action_rules.krb'):
           [1643932984.629554, 'bc_action_rules_bc.py'],
         ('', '', 'bc_action_rules_questions.krb'):
           [1643932984.6504989, 'bc_action_rules_questions_bc.py'],
         ('', '', 'bc_moto_rules.krb'):
           [1643932984.6784241, 'bc_moto_rules_bc.py'],
         ('', '', 'bc_moto_rules_questions.krb'):
           [1643932984.7043583, 'bc_moto_rules_questions_bc.py'],
         ('', '', 'moto_facts.kfb'):
           [1643932984.7053561, 'moto_facts.fbc'],
         ('', '', 'moto_questions.kqb'):
           [1643932984.7073505, 'moto_questions.qbc'],
         ('', '', 'pilot_questions.kqb'):
           [1643932984.7093453, 'pilot_questions.qbc'],
        },
        compiler_version)

