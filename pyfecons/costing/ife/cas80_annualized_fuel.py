from pyfecons.costing.calculations.interpolation import (
    interpolate_data,
    get_interpolated_value,
)
from pyfecons.costing.ife.pfr_costs import yearlytcost_pfr_coords
from pyfecons.costing.categories.cas800000 import CAS80
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def cas80_annualized_fuel_costs(basic: Basic) -> CAS80:
    # Cost Category 80: Annualized Fuel Cost (AFC)
    cas80 = CAS80()

    # Simple interpolation of yearly total target cost from interpolated grpah 2 below. See 22.1.8 for more.
    yearly_cost_interpolation = interpolate_data(yearlytcost_pfr_coords)
    cas80.C800000 = M_USD(
        get_interpolated_value(yearly_cost_interpolation, basic.implosion_frequency)
    )
    return cas80
