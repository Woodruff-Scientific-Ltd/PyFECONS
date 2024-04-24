from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider

CAS_200000_TEX = 'CAS200000.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict) -> list[TemplateProvider]:
    OUT = data.cas20
    # TODO - why are C210000 and C280000 counted twice?
    OUT.C200000 = M_USD(data.cas21.C210000 +
                        data.cas21.C210000 +
                        data.cas22.C220000 +
                        data.cas23.C230000 +
                        data.cas24.C240000 +
                        data.cas25.C250000 +
                        data.cas26.C260000 +
                        data.cas27.C270000 +
                        data.cas28.C280000 +
                        data.cas28.C280000 +
                        data.cas29.C290000)
    OUT.template_file = CAS_200000_TEX
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C200000': round(data.cas20.C200000)  # TODO - C200000 not in the template
    }
    return [OUT]

