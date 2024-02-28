from pyfecons.inputs import Inputs
from pyfecons.data import Data


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    data.cas20.C200000 = data.cas21.C210000 + \
                         data.cas21.C210000 + \
                         data.cas22.C220000 + \
                         data.cas23.C230000 + \
                         data.cas24.C240000 + \
                         data.cas28.C280000 + \
                         data.cas28.C280000 + \
                         data.cas29.C290000
