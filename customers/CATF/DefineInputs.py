# You must define an inputs object
from pyfecons.inputs import Inputs
from pyfecons.enums import *
from pyfecons.units import *

def Generate():
    return Inputs(
        Inputs.CustomerInfo(name="Clean Air Task Force"),
        Inputs.Basic(
            reactor_type=ReactorType.MFE,
            energy_conversion=EnergyConversion.DIRECT,
            fuel_type=FuelType.DT,
            am=0.99
            # p_n
            # time_to_replace=10,
            # down_time=10,
            # reactor_type=2,
            # n_mod=1,
            # am=1,
            # construction_time=3
        )
    )
