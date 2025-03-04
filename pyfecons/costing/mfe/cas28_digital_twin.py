from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


def cas28_digital_twin_costs(inputs: AllInputs, data: Data) -> TemplateProvider:
    # cost category 28 Digital Twin
    OUT = data.cas28
    # In-house cost estimate provided by NtTau Digital LTD
    OUT.C280000 = M_USD(5)

    OUT.template_file = "CAS280000.tex"
    OUT.replacements = {"C280000": str(data.cas28.C280000)}
    return OUT
