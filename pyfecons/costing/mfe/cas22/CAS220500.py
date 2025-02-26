from pyfecons.costing.calculations.cas22.cas220500_fuel_handling_and_storage import (
    compute_fuel_handling_and_storage_costs,
    compute_replacements,
)
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs


def cas_2205_fuel_handling_and_storage(
    inputs: AllInputs, data: Data
) -> TemplateProvider:
    # Cost Category 22.5 Fuel Handling and Storage
    IN = inputs.fuel_handling
    OUT = data.cas2205
    OUT = compute_fuel_handling_and_storage_costs(IN, OUT)

    OUT.template_file = "CAS220500_DT.tex"
    OUT.replacements = compute_replacements(IN, OUT)
    return OUT
