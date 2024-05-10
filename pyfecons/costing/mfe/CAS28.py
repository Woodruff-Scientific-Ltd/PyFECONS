from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.units import M_USD

CAS_280000_TEX = 'CAS280000.tex'


def GenerateData(inputs: Inputs, data: Data) -> list[TemplateProvider]:
    # cost category 28 Digital Twin
    OUT = data.cas28
    # In-house cost estimate provided by NtTau Digital LTD
    OUT.C280000 = M_USD(5)

    OUT.template_file = CAS_280000_TEX
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C280000': str(data.cas28.C280000)
    }
    return [OUT]