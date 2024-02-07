from pyfecons.inputs import Inputs
from pyfecons.data import Data
def GenerateData(inputs: Inputs, data: Data, figures: dict):
    data.cas26.C260000 = round(inputs.basic.n_mod * data.power_table.p_et * 0.107 * 1.15, 1)