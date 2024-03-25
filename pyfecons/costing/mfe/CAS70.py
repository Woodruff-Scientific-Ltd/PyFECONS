from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    OUT = data.cas70

    # Cost Category  70 Annualized O\&M Cost (AOC)
    c_om = 60 * data.power_table.p_net * 1000

    # C750000 = 0.1 * (C220000) scheduled replacement costs

    OUT.C700000 = M_USD(c_om/1e6)  # + C750000
