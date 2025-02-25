from pyfecons.units import M_USD
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs


def cas_28(inputs: AllInputs, data: Data) -> TemplateProvider:
    # Cost Category 28 Digital Twin
    OUT = data.cas28
    # In-house cost estimate provided by NtTau Digital LTD
    OUT.C280000 = M_USD(5)
    OUT.template_file = "CAS280000.tex"
    OUT.replacements = {"C280000": round(OUT.C280000)}
    return OUT
