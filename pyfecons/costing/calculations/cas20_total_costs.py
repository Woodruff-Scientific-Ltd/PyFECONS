from pyfecons.costing.categories.cas200000 import CAS20
from pyfecons.units import M_USD


def cas20_total_costs(cas2x_total_cost: M_USD) -> CAS20:
    cas20 = CAS20()
    cas20.C200000 = cas2x_total_cost
    cas20.template_file = "CAS200000.tex"
    cas20.replacements = {"C200000": round(cas20.C200000)}  # TODO - not in the template
    return cas20
