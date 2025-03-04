from pyfecons.data import CAS28
from pyfecons.units import M_USD


def cas28_digital_twin_costs() -> CAS28:
    # cost category 28 Digital Twin
    cas28 = CAS28()
    # In-house cost estimate provided by NtTau Digital LTD
    cas28.C280000 = M_USD(5)

    cas28.template_file = "CAS280000.tex"
    cas28.replacements = {"C280000": str(cas28.C280000)}
    return cas28
