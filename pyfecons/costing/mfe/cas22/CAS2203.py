from pyfecons.costing.calculations.conversions import inflation_1992_2024
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.units import M_USD


def cas_2203_auxilary_cooling(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.3  Auxiliary cooling
    OUT = data.cas2203
    # Auxiliary cooling systems
    OUT.C220300 = M_USD(1.10 * 1e-3 * float(inputs.basic.n_mod) * data.power_table.p_th * inflation_1992_2024)
    OUT.template_file = 'CAS220300.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C220300': str(round(OUT.C220300, 1))
    }
    return OUT
