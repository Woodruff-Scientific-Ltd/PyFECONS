from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data

CAS_700000_TEX = 'CAS700000.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    # Cost Category  70 Annualized O\&M Cost (AOC)
    OUT = data.cas70

    c_om = 60 * data.power_table.p_net * 1000

    # TODO what's up with the commented code here?
    # C750000 = 0.1 * (C220000) scheduled replacement costs

    OUT.C700000 = M_USD(c_om/1e6)  # + C750000

    OUT.template_file = CAS_700000_TEX
    OUT.replacements = {
        'C700000': round(data.cas70.C700000)
    }
