from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data

CAS_230000_TEX = 'CAS230000.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    # Cost Category 23 Turbine Plant Equipment
    OUT = data.cas23
    # TODO what are the constants 0.219 and 1.15?
    OUT.C230000 = M_USD(float(inputs.basic.n_mod) * data.power_table.p_et * 0.219 * 1.15)

    OUT.template_file = CAS_230000_TEX
    OUT.replacements = {
        'C230000': round(data.cas23.C230000, 1)
    }
