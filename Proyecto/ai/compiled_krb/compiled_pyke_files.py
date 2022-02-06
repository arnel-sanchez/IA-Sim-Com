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
           [1644108127.5176504, 'action_facts.fbc'],
         ('', '', 'action_questions.kqb'):
           [1644108127.5446353, 'action_questions.qbc'],
         ('', '', 'bc_action_rules.krb'):
           [1644108127.5646229, 'bc_action_rules_bc.py'],
         ('', '', 'bc_action_rules_questions.krb'):
           [1644108127.580614, 'bc_action_rules_questions_bc.py'],
         ('', '', 'bc_moto_rules.krb'):
           [1644108127.5976012, 'bc_moto_rules_bc.py'],
         ('', '', 'bc_moto_rules_questions.krb'):
           [1644108127.6125934, 'bc_moto_rules_questions_bc.py'],
         ('', '', 'moto_facts.kfb'):
           [1644108127.615591, 'moto_facts.fbc'],
         ('', '', 'moto_questions.kqb'):
           [1644108127.619589, 'moto_questions.qbc'],
        },
        compiler_version)

