from pyfecons import M_USD
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def GenerateData(inputs: Inputs, data: Data) -> list[TemplateProvider]:
    # Cost Category 25 Miscellaneous Plant Equipment
    OUT = data.cas25

    # factor of 1.15 obtained from escalating relative to 2019 $
    # TODO move to inflation constant
    OUT.C250000 = M_USD(float(inputs.basic.n_mod) * data.power_table.p_et * 0.038 * 1.15)

    OUT.template_file = 'CAS250000.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C250000': round(OUT.C250000)
    }
    return [OUT]