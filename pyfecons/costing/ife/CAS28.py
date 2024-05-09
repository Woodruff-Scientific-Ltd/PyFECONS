from pyfecons.units import M_USD
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def GenerateData(inputs: Inputs, data: Data) -> list[TemplateProvider]:
    # Cost Category 28 Digital Twin
    OUT = data.cas28
    # In-house cost estimate provided by NtTau Digital LTD
    OUT.C280000 = M_USD(5)
    OUT.template_file = 'CAS280000.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C280000': round(OUT.C280000)
    }
    return [OUT]