from pyfecons.inputs import Inputs
from pyfecons.data import Data


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    # Cost Category 29 Contingency
    data.cas29.C290000 = round(data.cas21.C210000
                               + data.cas22.C220000
                               + data.cas23.C230000
                               + data.cas24.C240000
                               + data.cas28.C280000
                               + data.cas28.C280000, 1)

    # TODO - This one adds CAS28 twice - ask Alex why