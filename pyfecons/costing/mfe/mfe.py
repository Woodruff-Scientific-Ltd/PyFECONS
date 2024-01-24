from typing import Dict

from pyfecons.inputs import Inputs
from pyfecons.data import Data
from pyfecons.costing.mfe.power import GenerateData as PowerBalanceData
from pyfecons.costing.mfe.CAS10 import GenerateData as CAS10Data
from pyfecons.costing.mfe.CAS21 import GenerateData as CAS21Data
from pyfecons.costing.mfe.CAS22 import GenerateData as CAS22Data


def GenerateData(inputs: Inputs) -> Data:
    data = Data()
    figures = {}
    PowerBalanceData(inputs, data, figures)
    CAS10Data(inputs, data, figures)
    CAS21Data(inputs, data, figures)
    CAS22Data(inputs, data, figures)
    return data


def HydrateTemplates(inputs: Inputs, data: Data) -> Dict:
    return {"": ""}
