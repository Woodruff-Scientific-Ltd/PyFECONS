from pyfecons.inputs import *
from pyfecons.enums import *
from pyfecons.units import *


def Generate():
    return Inputs(
        CustomerInfo(name="Clean Air Task Force"),
        Basic(
            reactor_type=ReactorType.IFE,
            energy_conversion=EnergyConversion.DIRECT,
            fuel_type=FuelType.PB11,
            time_to_replace=Years(10),
            downtime=Years(1),
            n_mod=Count(1),
            am=Percent(1),
            construction_time=Years(6),
            plant_lifetime=Years(30),
            yearly_inflation=Percent(0.0245),
            plant_availability=Percent(0.9),
            noak=True,
            implosion_frequency=HZ(1),
        ),
        blanket=Blanket(
            first_wall=BlanketFirstWall.LIQUID_LITHIUM,
            blanket_type=BlanketType.FLOWING_LIQUID_FIRST_WALL,
            primary_coolant=BlanketPrimaryCoolant.LEAD_LITHIUM_PBLI,
            secondary_coolant=BlanketSecondaryCoolant.WATER,
            neutron_multiplier=BlanketNeutronMultiplier.PB_AS_PART_OF_PBLI,
            structure=BlanketStructure.FERRITIC_MARTENSITIC_STEEL_FMS,
        ),
    )
