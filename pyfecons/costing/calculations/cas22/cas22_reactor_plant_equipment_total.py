from pyfecons.costing.categories.cas220000 import CAS22
from pyfecons.units import M_USD


def cas22_reactor_plant_equipment_total_costs(
    cas2201_total_cost: M_USD, cas2200_total_cost: M_USD
) -> CAS22:
    # Reactor Plant Equipment (RPE) total
    cas22 = CAS22()

    # Cost category 22.1 total
    cas22.C220100 = cas2201_total_cost
    # Cost category 22.2 total
    cas22.C220000 = cas2200_total_cost
    return cas22
