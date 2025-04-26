from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.categories.cas220200 import CAS2202
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.blanket import Blanket
from pyfecons.units import Count, MW, M_USD

# TODO - review this section since there is lots of commented code


def cas_2202_main_and_secondary_coolant_costs(
    basic: Basic, power_table: PowerTable
) -> CAS2202:
    # MAIN AND SECONDARY COOLANT Cost Category 22.2
    cas2202 = CAS2202()
    cas2202.C220201 = compute_primary_coolant_costs(basic.n_mod, power_table.p_net)
    cas2202.C220202 = compute_intermediate_coolant_costs(power_table.p_th)
    cas2202.C220203 = compute_secondary_coolant_costs()
    # Main heat-transfer system (NSSS)
    cas2202.C220200 = M_USD(cas2202.C220201 + cas2202.C220202 + cas2202.C220203)
    return cas2202


def compute_primary_coolant_costs(n_mod: Count, p_net: MW) -> M_USD:
    # Li(f), PbLi, He:                %Primary coolant(i):
    # C_22_2_1  = 233.9 * (PTH/3500)^0.55

    # am assuming a linear scaling	%Li(f), PbLi, He:
    # C220201  = 268.5  * (float(basic.n_mod) * power_table.p_th / 3500) * inflation_1992_2024

    # Primary coolant(i):  1.85 is due to inflation%the CPI scaling of 1.71 comes from:
    # https://www.bls.gov/data/inflation_calculator.htm scaled relative to 1992 dollars (despite 2003 publication date)
    # this is the Sheffield cost for a 1GWe system
    return M_USD(166 * (float(n_mod) * p_net / 1000))


def compute_intermediate_coolant_costs(p_th: MW) -> M_USD:
    # OC, H2O(g)
    # C_22_2_1  = 75.0 * (PTH/3500)^0.55
    # Intermediate coolant system
    return M_USD(40.6 * (p_th / 3500) ** 0.55)


def compute_secondary_coolant_costs() -> M_USD:
    # Secondary coolant system
    # 75.0 * (PTH/3500)^0.55
    return M_USD(0)
