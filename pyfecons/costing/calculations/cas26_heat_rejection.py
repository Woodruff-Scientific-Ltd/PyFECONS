from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.calculations.conversions import inflation_factor_2019_2024
from pyfecons.costing.categories.cas260000 import CAS26
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def cas26_heat_rejection_costs(basic: Basic, power_table: PowerTable) -> CAS26:
    # Cost Category 26 Heat Rejection
    cas26 = CAS26()

    # heat rejection scaled as NET electric power escalated relative to 2019 dollars to 2026 dollars
    cas26.C260000 = M_USD(
        float(basic.n_mod) * power_table.p_et * 0.107 * inflation_factor_2019_2024
    )

    cas26.template_file = "CAS260000.tex"
    cas26.replacements = {"C260000": round(cas26.C260000, 1)}
    return cas26
