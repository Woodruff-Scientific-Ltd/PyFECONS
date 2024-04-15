from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data

CAS_250000_TEX = 'CAS250000.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    # Cost Category 25 Miscellaneous Plant Equipment
    OUT = data.cas25
    # factor of 1.15 obtained from escalating relative to $ 2019
    # TODO where does 0.038 come from? Can we extract 1.15 to an input parameter?
    OUT.C250000 = M_USD(float(inputs.basic.n_mod) * data.power_table.p_et * 0.038 * 1.15)

    OUT.template_file = CAS_250000_TEX
    OUT.replacements = {
        'C250000': round(data.cas25.C250000, 1)
    }