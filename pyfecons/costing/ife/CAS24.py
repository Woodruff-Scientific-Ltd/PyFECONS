from pyfecons.units import M_USD
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def cas_24(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 24 Electric Plant Equipment
    OUT = data.cas24
    # TODO - where do constants come from?
    OUT.C240000 = M_USD(
        float(inputs.basic.n_mod) * data.power_table.p_et * 0.054 * 1.15
    )

    OUT.template_file = "CAS240000.tex"
    OUT.replacements = {"C240000": round(OUT.C240000)}
    return OUT
