import numpy as np

from pyfecons.inputs import *
from pyfecons.enums import *
from pyfecons.units import *


def Generate():
    p_nrl = MW(2500)  # Fusion Power
    p_implosion = MW(10)  # Implosion laser power
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
        radial_build=RadialBuild(
            # Radial thicknesses of concentric components (innermost to outermost)
            axis_t=Meters(0),  # distance from r=0 to plasma central axis
            plasma_t=Meters(0.0001),  # plasma radial thickness
            vacuum_t=Meters(8.48),  # vacuum radial thickness
            firstwall_t=Meters(0.005),  # first wall radial thickness
            blanket1_t=Meters(0),  # blanket radial thickness
            reflector_t=Meters(0.1),  # reflector radial thickness
            ht_shield_t=Meters(0.1),  # High-temperature shield radial thickness
            structure_t=Meters(0.2),  # support structure radial thickness
            gap1_t=Meters(0.5),  # air gap radial thickness
            vessel_t=Meters(0.2),  # vacuum vessel wall radial thickness
            gap2_t=Meters(0.5),  # second air gap radial thickness
            lt_shield_t=Meters(0.3),  # low-temperature shield radial thickness
            bioshield_t=Meters(1),  # concrete bioshield radial thickness
        ),
        # TODO clarify where shield fractions come from
        shield=Shield(
            f_SiC=Ratio(0.00),
            FPCPPFbLi=Ratio(0.1),
            f_W=Ratio(0.00),
            f_BFS=Ratio(0.9),
        ),
        lasers=Lasers(
            beamlet_learning_curve=Ratio(5),
            beamlet_learning_curve_coefficient_b=Ratio(np.log(1/5) / np.log(288)),
            nif_laser_energy=MJ(4.7),
        ),
        lsa_levels=LsaLevels(
            lsa=2
        ),
        primary_structure=PrimaryStructure(
            syst_pga=StructurePga.PGA_01,
            learning_credit=Ratio(0.5)
        ),
        vacuum_system=VacuumSystem(
            t_cool=K(20),
            t_env=K(300),
            ves_mfr=Ratio(10),
            beam_cs_area=Meters2(0.03),
            factor_of_safety=Ratio(3),
            geometry_factor=Ratio(10),
            beam_length=Meters(5),
            # assume 1 second vac rate
            # cost of 1 vacuum pump, scaled from 1985 dollars
            cost_pump=USD(40000),
            # 48 pumps needed for 200^3 system
            # capable of beign pumped by 1 pump
            vpump_cap=Meters3(200/48)
        ),
        power_supplies=PowerSupplies(
            # 1$/W power supply rule of thumb
            cost_per_watt=USD_W(1),
            p_compress=Unknown(1),
            learning_credit=Ratio(0.5),
            cap_temp=K(60),
            cap_temp_ambient=K(20),
            cap_temp_delta=K(30),
            cap_voltage=V(20000),
            cap_l1=Unknown(50000),
        ),
        target_factory=TargetFactory(
            learning_credit=Ratio(0.8)
        ),
        direct_energy_converter=DirectEnergyConverter(
            system_power=Unknown(1),
            flux_limit=Unknown(2),
        ),
        installation=Installation(
            labor_rate=USD(1600)
        ),
        fuel_handling=FuelHandling(
            learning_curve_credit=Ratio(0.8)
        ),
        npv=NpvInput(
            discount_rate=Percent(0.08)
        ),
    )
