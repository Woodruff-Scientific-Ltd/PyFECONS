from pyfecons.inputs import Inputs
from pyfecons.data import Data

CAS_240000_TEX = 'CAS240000.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    # Cost Category 24 Electric Plant Equipment
    # TODO what do 0.054 & 1.15 represent?
    data.cas24.C240000 = float(inputs.basic.n_mod) * data.power_table.p_et * 0.054 * 1.15

    data.cas24.template_file = CAS_240000_TEX
    data.cas24.replacements = {
        'C240000': round(data.cas24.C240000, 1)
    }