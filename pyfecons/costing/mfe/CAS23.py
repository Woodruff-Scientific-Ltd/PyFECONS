from pyfecons.inputs import Inputs
from pyfecons.data import Data
def GenerateData(inputs: Inputs, data: Data, figures: dict):
    data.cas23.C230000 = round(inputs.basic.n_mod * data.power_table.p_et * 3.19 * 1.15, 1)