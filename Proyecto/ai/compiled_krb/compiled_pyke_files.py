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
           [1644800810.304302, 'action_facts.fbc'],
         ('', '', 'bc_action_rules.krb'):
           [1644800810.3133092, 'bc_action_rules_bc.py'],
         ('', '', 'bc_moto_rules.krb'):
           [1644800810.3302336, 'bc_moto_rules_bc.py'],
         ('', '', 'moto_facts.kfb'):
           [1644800810.3312302, 'moto_facts.fbc'],
        },
        compiler_version)

