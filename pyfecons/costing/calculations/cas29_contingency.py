from pyfecons.data import CAS29
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def cas29_contingency_costs(basic: Basic, cas2X_total_cost: M_USD) -> CAS29:
    # Cost Category 29 Contingency
    cas29 = CAS29()
    if basic.noak:
        cas29.C290000 = M_USD(0)
    else:
        # TODO what is the 0.1? Should it be an input?
        cas29.C290000 = M_USD(0.1 * cas2X_total_cost)

    cas29.template_file = "CAS290000.tex"
    cas29.replacements = {"C290000": round(cas29.C290000)}
    return cas29
