from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    OUT = data.cas90

    # Cost Category 90: Annualized Financial Costs (AFC)
    # Total Capital costs 99
    OUT.C990000 = M_USD(data.cas10.C100000 + data.cas20.C200000 + data.cas30.C300000
                        + data.cas40.C400000 + data.cas50.C500000 + data.cas60.C600000)

    f_cr = 0.09   # Capital return factor
    OUT.C900000 = M_USD(f_cr * OUT.C990000)
