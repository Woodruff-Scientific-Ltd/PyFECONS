from pyfecons.costing.categories.cas200000 import CAS20
from pyfecons.units import M_USD


def cas20_total_costs(cas2x_total_cost: M_USD) -> CAS20:
    cas20 = CAS20()
    cas20.C200000 = cas2x_total_cost
    return cas20
