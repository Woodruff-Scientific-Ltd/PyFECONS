from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.units import M_USD


def cas_20(inputs: AllInputs, data: Data) -> TemplateProvider:
    OUT = data.cas20
    # TODO - why are C210000 and C280000 counted twice?
    OUT.C200000 = M_USD(
        data.cas21.C210000
        + data.cas21.C210000
        + data.cas22.C220000
        + data.cas23.C230000
        + data.cas24.C240000
        + data.cas25.C250000
        + data.cas26.C260000
        + data.cas27.C270000
        + data.cas28.C280000
        + data.cas28.C280000
        + data.cas29.C290000
    )
    OUT.template_file = "CAS200000.tex"
    OUT.replacements = {"C200000": round(OUT.C200000)}  # TODO - not in the template
    return OUT
