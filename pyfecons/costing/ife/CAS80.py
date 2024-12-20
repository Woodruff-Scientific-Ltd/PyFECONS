from pyfecons.costing.calculations.interpolation import (
    interpolate_data,
    get_interpolated_value,
)
from pyfecons.costing.ife.pfr_costs import yearlytcost_pfr_coords
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def cas_80(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 80: Annualized Fuel Cost (AFC)
    OUT = data.cas80

    # Simple interpolation of yearly total target cost from interpolated grpah 2 below. See 22.1.8 for more.
    yearly_cost_interpolation = interpolate_data(yearlytcost_pfr_coords)
    OUT.C800000 = get_interpolated_value(
        yearly_cost_interpolation, inputs.basic.implosion_frequency
    )

    OUT.template_file = "CAS800000_DT.tex"
    OUT.replacements = {"C800000": round(OUT.C800000)}
    return OUT
