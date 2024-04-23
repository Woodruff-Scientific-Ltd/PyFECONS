from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider

CAS_260000_TEX = 'CAS260000.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict) -> list[TemplateProvider]:
    # Cost Category 26 Heat Rejection
    OUT = data.cas26
    # heat rejection scaled as NET electric power escalated relative to 2019 dollars to 2026 dollars
    # TODO what is 0.107?
    OUT.C260000 = M_USD(float(inputs.basic.n_mod) * data.power_table.p_et * 0.107 * 1.15)

    OUT.template_file = CAS_260000_TEX
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C260000': round(data.cas26.C260000, 1)
    }
    return [OUT]