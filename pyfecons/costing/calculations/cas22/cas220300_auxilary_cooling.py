from pyfecons.costing.calculations.conversions import inflation_1992_2024
from pyfecons.units import Count, MW, M_USD


def compute_auxilary_coolant_costs(n_mod: Count, p_th: MW) -> M_USD:
    # Auxiliary cooling systems
    return M_USD(1.10 * 1e-3 * float(n_mod) * p_th * inflation_1992_2024)
