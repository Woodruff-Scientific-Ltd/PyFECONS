from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.units import M_USD


def cas_26(inputs: AllInputs, data: Data) -> TemplateProvider:
    # Cost Category 26 Heat Rejection
    OUT = data.cas26

    # heat rejection scaled as NET electric power escalated relative to 2019 dollars to 2026 dollars
    # TODO create inflation variable, what is 0.107?
    OUT.C260000 = M_USD(
        float(inputs.basic.n_mod) * data.power_table.p_net * 0.107 * 1.15
    )

    OUT.template_file = "CAS260000.tex"
    OUT.replacements = {"C260000": round(OUT.C260000)}
    return OUT
