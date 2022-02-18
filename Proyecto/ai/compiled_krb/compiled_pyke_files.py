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
           [1645145079.395172, 'action_facts.fbc'],
         ('', '', 'bc_action_rules.krb'):
           [1645145079.4402812, 'bc_action_rules_bc.py'],
         ('', '', 'bc_moto_rules.krb'):
           [1645145079.4620032, 'bc_moto_rules_bc.py'],
         ('', '', 'moto_facts.kfb'):
           [1645145079.4638093, 'moto_facts.fbc'],
        },
        compiler_version)

