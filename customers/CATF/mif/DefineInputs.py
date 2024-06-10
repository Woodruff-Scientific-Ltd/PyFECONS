# You must define an inputs object
from pyfecons.inputs import *
from pyfecons.enums import *
from pyfecons.units import *


def Generate():
    return Inputs(
        CustomerInfo(name="Clean Air Task Force"),
        Basic(
            reactor_type=ReactorType.MIF,
            confinement_type=ConfinementType.MIRROR_MIF,
            energy_conversion=EnergyConversion.DIRECT,
            # fuel_type=FuelType.DT,
            p_nrl=MW(2600.0),
            n_mod=Count(1),
            am=Percent(1),
            downtime=Years(1),
            construction_time=Years(3),
            plant_lifetime=Years(30),
            plant_availability=Percent(0.85),
            yearly_inflation=Percent(0.0245),
            time_to_replace=Years(10),
        ),
    )
