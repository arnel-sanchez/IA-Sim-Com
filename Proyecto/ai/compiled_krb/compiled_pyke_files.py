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
           [1644093881.5992475, 'action_facts.fbc'],
         ('', '', 'action_questions.kqb'):
           [1644093881.6215186, 'action_questions.qbc'],
         ('', '', 'bc_action_rules.krb'):
           [1644093881.6435046, 'bc_action_rules_bc.py'],
         ('', '', 'bc_action_rules_questions.krb'):
           [1644093881.6644924, 'bc_action_rules_questions_bc.py'],
         ('', '', 'bc_moto_rules.krb'):
           [1644093881.6894755, 'bc_moto_rules_bc.py'],
         ('', '', 'bc_moto_rules_questions.krb'):
           [1644093881.7174592, 'bc_moto_rules_questions_bc.py'],
         ('', '', 'moto_facts.kfb'):
           [1644093881.7294524, 'moto_facts.fbc'],
         ('', '', 'moto_questions.kqb'):
           [1644093881.73245, 'moto_questions.qbc'],
        },
        compiler_version)

