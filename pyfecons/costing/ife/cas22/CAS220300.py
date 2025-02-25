from pyfecons.costing.calculations.cas22.cas220300_auxilary_cooling import (
    compute_auxilary_coolant_costs,
)
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs


def cas_2203_auxilary_cooling(inputs: AllInputs, data: Data) -> TemplateProvider:
    # Cost Category 22.3  Auxiliary cooling
    OUT = data.cas2203
    OUT.C220300 = compute_auxilary_coolant_costs(
        inputs.basic.n_mod, data.power_table.p_th
    )
    OUT.template_file = "CAS220300.tex"
    OUT.replacements = {"C220300": str(round(OUT.C220300, 1))}
    return OUT
