from pyfecons.inputs import *
from pyfecons.enums import *
from pyfecons.units import *


def Generate():
    p_nrl = MW(2500)  # Fusion Power
    p_implosion = MW(10) # Implosion laser power
    p_ignition = MW(0.1)  # Ignition laser power
    return Inputs(
        CustomerInfo(name="Clean Air Task Force"),
        Basic(
            reactor_type=ReactorType.IFE,
            confinement_type=ConfinementType.LASER_DRIVEN_DIRECT_DRIVE,
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
            p_nrl=p_nrl,
        ),
        blanket=Blanket(
            first_wall=BlanketFirstWall.LIQUID_LITHIUM,
            blanket_type=BlanketType.FLOWING_LIQUID_FIRST_WALL,
            primary_coolant=BlanketPrimaryCoolant.LITHIUM_LI,
            secondary_coolant=BlanketSecondaryCoolant.WATER,
            neutron_multiplier=BlanketNeutronMultiplier.PB_AS_PART_OF_PBLI,
            structure=BlanketStructure.FERRITIC_MARTENSITIC_STEEL_FMS,
        ),
        power_table=PowerTable(
            mn=Ratio(1.09),  # Neutron energy multiplier
            eta_p=Percent(0.5),  # Pumping power capture efficiency
            fpcppf=Percent(0.01),  # Primary Coolant Pumping Power Fraction
            f_sub=Percent(0.01),  # Subsystem and Control Fraction
            p_trit=MW(6.3),  # Tritium Systems
            p_house=MW(4 * 300 / 560),  # Housekeeping power,
            p_cryo=MW(0.8 * p_nrl / 560),  # Cryo vacuum pumping
            eta_pin1=Percent(0.1),  # Input power wall plug efficiency (implosion)
            eta_pin2=Percent(0.1),  # Input power wall plug efficiency (ignition)
            eta_th=Percent(0.46),  # Thermal conversion efficiency
            p_implosion=p_implosion,
            p_ignition=p_ignition,
            p_input=MW(p_implosion + p_ignition),  # Input power
            p_target=MW(1),  # Power into target factory
            p_machinery=MW(1),  # Power into machinery
        ),
        lsa_levels=LsaLevels(
            lsa=2
        )
    )
