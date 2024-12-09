from pyfecons.costing.calculations.cas22.cas220109_direct_energy_converter import (
    get_subsystem_costs,
    get_scaled_costs,
    get_replacements,
)
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.units import M_USD


def cas_220109_direct_energy_converter(inputs: Inputs, data: Data) -> TemplateProvider:
    # 22.1.9 Direct Energy Converter
    IN = inputs.direct_energy_converter
    OUT = data.cas220109

    OUT.costs = get_subsystem_costs(inputs.basic.noak)
    OUT.scaled_costs = get_scaled_costs(OUT.costs, IN)

    # TODO verify this right now the script pulls "totaldecost": 591, which is not the sum of the parts
    # OUT.C220109 = M_USD(sum(OUT.scaled_costs.values()))
    # TODO why is this zero?
    OUT.C220109 = M_USD(0)

    OUT.template_file = "CAS220109.tex"
    OUT.replacements = get_replacements(OUT)
    return OUT
