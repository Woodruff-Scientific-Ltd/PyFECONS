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
            first_wall=BlanketFirstWall.BERYLLIUM,
            blanket_type=BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3,
            primary_coolant=BlanketPrimaryCoolant.LITHIUM_LI,
            secondary_coolant=BlanketSecondaryCoolant.LEAD_LITHIUM_PBLI,
            neutron_multiplier=BlanketNeutronMultiplier.BE12TI,
            structure=BlanketStructure.FERRITIC_MARTENSITIC_STEEL_FMS,
        ),
        coils=Coils(magnets=[
            Magnet(name="Coil 1", coil_count=1, j_cable=MA(21.4), r_centre=1.75, z_centre=0, dr=1, dz=1),
            Magnet(name="Coil 2", coil_count=2, j_cable=MA(22.4), r_centre=2.75, z_centre=1, dr=2, dz=2),
            Magnet(name="Coil 3", coil_count=3, j_cable=MA(23.4), r_centre=3.75, z_centre=2, dr=3, dz=3),
        ]),
        primary_structure=PrimaryStructure(syst_pga=StructurePga.PGA_03, learning_credit=0.5)
    )
