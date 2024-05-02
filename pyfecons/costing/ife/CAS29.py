from pyfecons import M_USD
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def GenerateData(inputs: Inputs, data: Data) -> list[TemplateProvider]:
    # Cost Category 29 Contingency
    OUT = data.cas29
    if inputs.basic.noak:
        OUT.C290000 = M_USD(0)
    else:
        OUT.C290000 = M_USD(0.1 * (data.cas21.C210000 + data.cas22.C220000 + data.cas23.C230000 + data.cas24.C240000
                                   + data.cas25.C250000 + data.cas26.C260000 + data.cas27.C270000 + data.cas28.C280000))

    OUT.template_file = 'CAS290000.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C290000': round(OUT.C290000)
    }
    return [OUT]