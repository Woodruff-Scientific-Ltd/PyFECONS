from pyfecons.costing.calculations.cas22.cas220400_rad_waste import (
    compute_radioactive_waste_cost,
)
from pyfecons.data import Data, TemplateProvider


def cas_2204_radwaste(data: Data) -> TemplateProvider:
    # Cost Category 22.4 Radwaste
    OUT = data.cas2204
    OUT.C220400 = compute_radioactive_waste_cost(data.power_table.p_th)
    OUT.template_file = "CAS220400.tex"
    OUT.replacements = {"C220400": round(data.cas2204.C220400, 1)}
    return OUT
