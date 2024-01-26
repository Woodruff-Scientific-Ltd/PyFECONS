# You must define an inputs object
from pyfecons.inputs import *
from pyfecons.enums import *
from pyfecons.units import *


def Generate():
    return Inputs(
        CustomerInfo(name="Clean Air Task Force"),
        Basic(
            reactor_type=ReactorType.MFE,
            energy_conversion=EnergyConversion.DIRECT,
            fuel_type=FuelType.DT,
            am=Percent(0.99)
            # p_n
            # time_to_replace=10,
            # down_time=10,
            # reactor_type=2,
            # n_mod=1,
            # am=1,
            # construction_time=3
        ),
        blanket=Blanket(
            BlanketFirstWall.BERYLLIUM,
            BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3,
            BlanketPrimaryCoolant.LITHIUM_LI,
            BlanketSecondaryCoolant.OTHER_EUTECTIC_SALT,
            BlanketNeutronMultiplier.BE12TI,
            BlanketStructure.FERRITIC_MARTENSITIC_STEEL_FMS,
        )
    )
