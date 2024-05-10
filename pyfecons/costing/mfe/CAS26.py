from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.units import M_USD


def cas_26(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 26 Heat Rejection
    OUT = data.cas26
    # heat rejection scaled as NET electric power escalated relative to 2019 dollars to 2026 dollars
    OUT.C260000 = M_USD(float(inputs.basic.n_mod) * data.power_table.p_et * 0.107 * 1.15)

    OUT.template_file = 'CAS260000.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C260000': round(data.cas26.C260000, 1)
    }
    return OUT