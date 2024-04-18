# You must define an inputs object
from pyfecons.inputs import *
from pyfecons.enums import *
from pyfecons.units import *


def Generate():
    # TODO - need to extract tf_dr, radial build, and coils into a more defined construct
    tf_dr = Meters(0.25)  # Main toroidal field coil thickness
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
        radial_build=RadialBuild(coil_t=tf_dr),
        coils=Coils(magnets=[
            Magnet('TF', MagnetType.TF, MagnetMaterialType.HTS_CICC, 12, Meters(0.18), Meters(0), tf_dr, Meters(0.35), Ratio(0), 20, 5),
            Magnet('CS', MagnetType.CS, MagnetMaterialType.HTS_CICC, 1, Meters(0.18), Meters(0), Meters(0.2), Meters(6.3), Ratio(0), 20, 10),
            Magnet('PF1', MagnetType.PF, MagnetMaterialType.COPPER, 2, Meters(0.67), Meters(3.73), Meters(0.3), Meters(0.6), Ratio(0), 20, 2),
            Magnet('PF2', MagnetType.PF, MagnetMaterialType.HTS_CICC, 2, Meters(0.9), Meters(4.64), Meters(0.3), Meters(0.6), Ratio(0), 20, 2),
            Magnet('PF3', MagnetType.PF, MagnetMaterialType.HTS_CICC, 2, Meters(1.28), Meters(5.55), Meters(0.5), Meters(0.6), Ratio(0), 20, 2),
            Magnet('PF4', MagnetType.PF, MagnetMaterialType.HTS_CICC, 2, Meters(2.72), Meters(7.24), Meters(0.75), Meters(0.37), Ratio(0), 20, 2),
            Magnet('PF5', MagnetType.PF, MagnetMaterialType.HTS_CICC, 2, Meters(5.3), Meters(7.24), Meters(1.8), Meters(0.37), Ratio(0), 20, 2),
            Magnet('PF6', MagnetType.PF, MagnetMaterialType.HTS_PANCAKE, 2, Meters(9.34), Meters(5), Meters(1), Meters(1), Ratio(0), 20, 2),
            Magnet('PF7', MagnetType.PF, MagnetMaterialType.HTS_CICC, 2, Meters(9.34), Meters(3.6), Meters(1), Meters(1), Ratio(0), 20, 2, True, Meters(5), Meters(5)),
            Magnet('PF8', MagnetType.PF, MagnetMaterialType.HTS_CICC, 2, Meters(9.34), Meters(2.2), Meters(1), Meters(1), Ratio(0), 20, 2, True, Meters(5), Meters(5)),
        ]),
        primary_structure=PrimaryStructure(syst_pga=StructurePga.PGA_03, learning_credit=0.5),
    )
