from pyfecons.units import Count, MW, M_USD
# TODO - review this section since there is lots of commented code


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
