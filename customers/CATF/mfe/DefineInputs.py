# You must define an inputs object
from pyfecons.enums import *
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.blanket import Blanket
from pyfecons.inputs.coils import Coils
from pyfecons.inputs.customer_info import CustomerInfo
from pyfecons.inputs.direct_energy_converter import DirectEnergyConverter
from pyfecons.inputs.fuel_handling import FuelHandling
from pyfecons.inputs.installation import Installation
from pyfecons.inputs.lsa_levels import LsaLevels
from pyfecons.inputs.magnet import Magnet
from pyfecons.inputs.npv_Input import NpvInput
from pyfecons.inputs.power_supplies import PowerSupplies
from pyfecons.inputs.power_table_input import PowerTableInput
from pyfecons.inputs.primary_structure import PrimaryStructure
from pyfecons.inputs.radial_build import RadialBuild
from pyfecons.inputs.shield import Shield
from pyfecons.inputs.vacuum_system import VacuumSystem
from pyfecons.units import *


def Generate() -> AllInputs:
    # TODO - need to extract tf_dr, radial build, and coils into a more defined construct
    tf_dr = Meters(0.25)  # Main toroidal field coil thickness
    return AllInputs(
        customer_info=CustomerInfo(name="Clean Air Task Force"),
        basic=Basic(
            reactor_type=ReactorType.MFE,
            confinement_type=ConfinementType.SPHERICAL_TOKAMAK,
            energy_conversion=EnergyConversion.DIRECT,
            fuel_type=FuelType.DT,
            p_nrl=MW(2600.0),
            n_mod=Count(1),
            am=Percent(0.99),
            downtime=Years(1),
            construction_time=Years(6),
            plant_lifetime=Years(30),
            plant_availability=Percent(0.85),
            noak=True,
            yearly_inflation=Percent(0.0245),
            time_to_replace=Years(10),
        ),
        blanket=Blanket(
            first_wall=BlanketFirstWall.BERYLLIUM,
            blanket_type=BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3,
            primary_coolant=BlanketPrimaryCoolant.LITHIUM_LI,
            secondary_coolant=BlanketSecondaryCoolant.LEAD_LITHIUM_PBLI,
            neutron_multiplier=BlanketNeutronMultiplier.BE12TI,
            structure=BlanketStructure.FERRITIC_MARTENSITIC_STEEL_FMS,
        ),
        power_table=PowerTableInput(
            f_sub=Percent(0.03),
            p_cryo=MW(0.5),
            mn=Ratio(1.1),
            eta_p=Percent(0.5),
            eta_th=Percent(0.46),
            fpcppf=Percent(0.06),
            p_trit=MW(10),
            p_house=MW(4),
            p_tfcool=MW(12.7),
            p_pfcool=MW(1),
            p_tf=MW(1),
            p_pf=MW(1),
            eta_pin=Percent(0.5),
            eta_pin1=Percent(0.18),
            eta_pin2=Percent(0.82),
            eta_de=Percent(0.85),
            p_input=MW(50),
        ),
        radial_build=RadialBuild(
            elon=Ratio(3),
            axis_t=Meters(3),
            plasma_t=Meters(1.1),
            vacuum_t=Meters(0.1),
            firstwall_t=Meters(0.2),
            blanket1_t=Meters(0.8),
            reflector_t=Meters(0.2),
            ht_shield_t=Meters(0.2),
            structure_t=Meters(0.2),
            gap1_t=Meters(0.5),
            vessel_t=Meters(0.2),
            coil_t=tf_dr,
            gap2_t=Meters(0.5),
            lt_shield_t=Meters(0.3),
            bioshield_t=Meters(1),
        ),
        # TODO clarify where shield fractions come from
        shield=Shield(
            f_SiC=Ratio(0.00),
            FPCPPFbLi=Ratio(0.1),
            f_W=Ratio(0.00),
            f_BFS=Ratio(0.9),
        ),
        coils=Coils(
            magnets=[
                Magnet(
                    "TF",
                    MagnetType.TF,
                    MagnetMaterialType.HTS_CICC,
                    12,
                    Meters(0.18),
                    Meters(0),
                    tf_dr,
                    Meters(0.35),
                    Ratio(0),
                    20,
                    5,
                ),
                Magnet(
                    "CS",
                    MagnetType.CS,
                    MagnetMaterialType.HTS_CICC,
                    1,
                    Meters(0.18),
                    Meters(0),
                    Meters(0.2),
                    Meters(6.3),
                    Ratio(0),
                    20,
                    10,
                ),
                Magnet(
                    "PF1",
                    MagnetType.PF,
                    MagnetMaterialType.COPPER,
                    2,
                    Meters(0.67),
                    Meters(3.73),
                    Meters(0.3),
                    Meters(0.6),
                    Ratio(0),
                    20,
                    2,
                ),
                Magnet(
                    "PF2",
                    MagnetType.PF,
                    MagnetMaterialType.HTS_CICC,
                    2,
                    Meters(0.9),
                    Meters(4.64),
                    Meters(0.3),
                    Meters(0.6),
                    Ratio(0),
                    20,
                    2,
                ),
                Magnet(
                    "PF3",
                    MagnetType.PF,
                    MagnetMaterialType.HTS_CICC,
                    2,
                    Meters(1.28),
                    Meters(5.55),
                    Meters(0.5),
                    Meters(0.6),
                    Ratio(0),
                    20,
                    2,
                ),
                Magnet(
                    "PF4",
                    MagnetType.PF,
                    MagnetMaterialType.HTS_CICC,
                    2,
                    Meters(2.72),
                    Meters(7.24),
                    Meters(0.75),
                    Meters(0.37),
                    Ratio(0),
                    20,
                    2,
                ),
                Magnet(
                    "PF5",
                    MagnetType.PF,
                    MagnetMaterialType.HTS_CICC,
                    2,
                    Meters(5.3),
                    Meters(7.24),
                    Meters(1.8),
                    Meters(0.37),
                    Ratio(0),
                    20,
                    2,
                ),
                Magnet(
                    "PF6",
                    MagnetType.PF,
                    MagnetMaterialType.HTS_PANCAKE,
                    2,
                    Meters(9.34),
                    Meters(5),
                    Meters(1),
                    Meters(1),
                    Ratio(0),
                    20,
                    2,
                ),
                Magnet(
                    "PF7",
                    MagnetType.PF,
                    MagnetMaterialType.HTS_CICC,
                    2,
                    Meters(9.34),
                    Meters(3.6),
                    Meters(1),
                    Meters(1),
                    Ratio(0),
                    20,
                    2,
                    True,
                    Meters(5),
                    Meters(5),
                ),
                Magnet(
                    "PF8",
                    MagnetType.PF,
                    MagnetMaterialType.HTS_CICC,
                    2,
                    Meters(9.34),
                    Meters(2.2),
                    Meters(1),
                    Meters(1),
                    Ratio(0),
                    20,
                    2,
                    True,
                    Meters(5),
                    Meters(5),
                ),
            ]
        ),
        lsa_levels=LsaLevels(lsa=2),
        primary_structure=PrimaryStructure(
            syst_pga=StructurePga.PGA_03,
            learning_credit=Ratio(0.5),
            replacement_factor=Ratio(0.1),
        ),
        vacuum_system=VacuumSystem(
            learning_credit=Ratio(0.5),
            spool_ir=Meters(2.25),
            spool_or=Meters(3.15),
            door_irb=Meters(6),
            door_orb=Meters(6.25),
            door_irc=Meters(7.81),
            door_orc=Meters(8.06),
            spool_height=Meters(9),
            # assume 1 second vac rate
            # cost of 1 vacuum pump, scaled from 1985 dollars
            cost_pump=USD(40000),
            # 48 pumps needed for 200^3 system
            vpump_cap=Meters3(200 / 48),
        ),
        power_supplies=PowerSupplies(
            learning_credit=Ratio(0.5),
            # $1/W power supply industry rule of thumb
            cost_per_watt=USD_W(1),
        ),
        direct_energy_converter=DirectEnergyConverter(
            system_power=Unknown(1),
            flux_limit=Unknown(2),
        ),
        installation=Installation(labor_rate=USD(1600)),
        fuel_handling=FuelHandling(learning_curve_credit=Ratio(0.8)),
        npv=NpvInput(discount_rate=Percent(0.08)),
    )
