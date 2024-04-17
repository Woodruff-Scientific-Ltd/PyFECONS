from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data

CAS_900000_TEX = 'CAS900000.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    # Cost Category 90: Annualized Financial Costs (AFC)
    OUT = data.cas90

    # Total Capital costs 99
    OUT.C990000 = M_USD(data.cas10.C100000 + data.cas20.C200000 + data.cas30.C300000
                        + data.cas40.C400000 + data.cas50.C500000 + data.cas60.C600000)

    # TODO should this be an input?
    f_cr = 0.09   # Capital return factor
    OUT.C900000 = M_USD(f_cr * OUT.C990000)

    OUT.template_file = CAS_900000_TEX
    OUT.replacements = {
        'C900000': round(data.cas90.C900000)
    }