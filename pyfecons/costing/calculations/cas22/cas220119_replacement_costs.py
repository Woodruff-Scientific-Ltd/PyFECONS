from pyfecons.costing.calculations.cas22.CAS22 import compute_cas2201_total_costs
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.units import M_USD


def cas_220119_scheduled_replacement_costs(
    inputs: AllInputs, data: Data
) -> TemplateProvider:
    #  Cost category 22.1.19 Scheduled Replacement Cost
    OUT = data.cas220119
    OUT.C220119 = M_USD(
        0
    )  # This needs to be zero for the total_costs calculation to run
    OUT.C220119 = M_USD(
        compute_cas2201_total_costs(data) * inputs.primary_structure.replacement_factor
    )
    OUT.template_file = "CAS220119.tex"
    OUT.replacements = {"C220119": str(round(OUT.C220119))}
    return OUT
