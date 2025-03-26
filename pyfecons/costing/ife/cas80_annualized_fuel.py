from pyfecons.costing.calculations.interpolation import (
    interpolate_data,
    get_interpolated_value,
)
from pyfecons.costing.ife.pfr_costs import yearlytcost_pfr_coords
from pyfecons.costing.categories.cas800000 import CAS80
from pyfecons.inputs.basic import Basic


def cas80_annualized_fuel_costs(basic: Basic) -> CAS80:
    # Cost Category 80: Annualized Fuel Cost (AFC)
    cas80 = CAS80()

    # Simple interpolation of yearly total target cost from interpolated grpah 2 below. See 22.1.8 for more.
    yearly_cost_interpolation = interpolate_data(yearlytcost_pfr_coords)
    cas80.C800000 = get_interpolated_value(
        yearly_cost_interpolation, basic.implosion_frequency
    )

    cas80.template_file = "CAS800000_DT.tex"
    cas80.replacements = {"C800000": round(cas80.C800000)}
    return cas80
