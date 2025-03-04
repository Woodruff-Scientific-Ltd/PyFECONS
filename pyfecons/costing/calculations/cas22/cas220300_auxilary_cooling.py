from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.calculations.conversions import inflation_1992_2024
from pyfecons.costing.categories.cas220300 import CAS2203
from pyfecons.inputs.basic import Basic
from pyfecons.units import Count, MW, M_USD


def cas_2203_auxilary_cooling_costs(basic: Basic, power_table: PowerTable) -> CAS2203:
    # Cost Category 22.3  Auxiliary cooling
    cas2203 = CAS2203()
    cas2203.C220300 = compute_auxilary_coolant_costs(basic.n_mod, power_table.p_th)
    cas2203.template_file = "CAS220300.tex"
    cas2203.replacements = {"C220300": str(round(cas2203.C220300, 1))}
    return cas2203


def compute_auxilary_coolant_costs(n_mod: Count, p_th: MW) -> M_USD:
    # Auxiliary cooling systems
    return M_USD(1.10 * 1e-3 * float(n_mod) * p_th * inflation_1992_2024)
