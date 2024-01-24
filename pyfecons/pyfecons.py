from pyfecons.inputs import Inputs
from pyfecons.data import Data
from pyfecons.enums import *
from pyfecons.costing.mfe.mfe import GenerateData as GenerateMFEData
from pyfecons.costing.mfe.mfe import HydrateTemplates as GenerateMFETemplates


def RunCostingWithInput(inputs: Inputs):
    if inputs.basic.reactor_type == ReactorType.MFE:
        return GenerateMFEData(inputs)
    elif inputs.basic.reactor_type == ReactorType.MIF:
        raise NotImplementedError()
    elif inputs.basic.reactor_type == ReactorType.IFE:
        raise NotImplementedError()
    raise ValueError('Invalid basic reactor type')


def HydrateTemplates(inputs: Inputs, data: Data):
    if inputs.basic.reactor_type == ReactorType.MFE:
        return GenerateMFETemplates(inputs, data)
    elif inputs.basic.reactor_type == ReactorType.MIF:
        raise NotImplementedError()
    elif inputs.basic.reactor_type == ReactorType.IFE:
        raise NotImplementedError()
    raise ValueError('Invalid basic reactor type')
