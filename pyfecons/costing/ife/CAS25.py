from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.units import M_USD


def cas_25(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 25 Miscellaneous Plant Equipment
    OUT = data.cas25

    # factor of 1.15 obtained from escalating relative to 2019 $
    # TODO move to inflation constant
    OUT.C250000 = M_USD(
        float(inputs.basic.n_mod) * data.power_table.p_et * 0.038 * 1.15
    )

    OUT.template_file = "CAS250000.tex"
    OUT.replacements = {"C250000": round(OUT.C250000)}
    return OUT
