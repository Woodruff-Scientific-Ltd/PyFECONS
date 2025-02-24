from pyfecons.costing.calculations.cas22.cas220200_coolant import (
    compute_primary_coolant_costs,
    compute_intermediate_coolant_costs,
    compute_secondary_coolant_costs,
)
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.units import M_USD


def cas_2202_main_and_secondary_coolant(inputs: AllInputs, data: Data) -> TemplateProvider:
    # MAIN AND SECONDARY COOLANT Cost Category 22.2
    OUT = data.cas2202
    OUT.C220201 = compute_primary_coolant_costs(
        inputs.basic.n_mod, data.power_table.p_net
    )
    OUT.C220202 = compute_intermediate_coolant_costs(data.power_table.p_th)
    OUT.C220203 = compute_secondary_coolant_costs()
    # Main heat-transfer system (NSSS)
    OUT.C220200 = M_USD(OUT.C220201 + OUT.C220202 + OUT.C220203)

    OUT.template_file = "CAS220200_DT.tex"
    OUT.replacements = {
        "C220200": round(OUT.C220200),
        "C220201": round(OUT.C220201),
        "C220202": round(OUT.C220202),
        "C220203": round(OUT.C220203),  # TODO not in template
        "primaryC": inputs.blanket.primary_coolant.display_name,
        "secondaryC": inputs.blanket.secondary_coolant.display_name,
    }
    return OUT
