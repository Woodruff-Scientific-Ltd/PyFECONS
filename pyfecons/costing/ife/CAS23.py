from pyfecons.units import M_USD
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs


def cas_23(inputs: AllInputs, data: Data) -> TemplateProvider:
    # Cost Category 23 Turbine Plant Equipment
    OUT = data.cas23
    # TODO - where do constants come from?
    OUT.C230000 = M_USD(
        float(inputs.basic.n_mod) * data.power_table.p_et * 0.219 * 1.15
    )

    OUT.template_file = "CAS230000.tex"
    OUT.tex_path = "Modified/" + OUT.template_file
    OUT.replacements = {"C230000": round(OUT.C230000)}
    return OUT
