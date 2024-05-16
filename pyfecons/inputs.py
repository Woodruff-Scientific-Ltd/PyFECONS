import math
from dataclasses import dataclass, field
from typing import Optional

from pyfecons.enums import *
from pyfecons.units import *
from pyfecons.materials import Materials
from pyfecons.serializable import SerializableToJSON


# These classes will contain every possible input
# They will not contain information about which inputs will actually be used by the costing code and which ones won't
# The DefineInputs.py script in each customer folder is in charge of making sure all the appropriate inputs are set
# The costing code itself should throw appropriate errors when necessary inputs are not set
# The logical flow of inputs & inputs dependencies will be documented here
# https://docs.google.com/spreadsheets/d/115j-R-XZX9JI_VGt4AR7T3fZ91Qdmtc-WfEg_CpSlKE/edit?usp=sharing
# The units, descriptions, and expected values will also be documented on the spreadsheet

# The classes within Inputs must maintain their own toDict function
# In addition, the Inputs class itself maintains its own toDict function that calls upon the sublcasses

@dataclass
class CustomerInfo:
    name: str = ''


@dataclass
class Basic:
    reactor_type: ReactorType = None
    confinement_type: ConfinementType = None
    energy_conversion: EnergyConversion = None
    fuel_type: FuelType = FuelType.DT
    p_nrl: MW = None  # Fusion Power
    n_mod: Count = None
    am: Percent = None
    downtime: Years = None
    construction_time: Years = None
    plant_lifetime: Years = None  # from end of construction
    plant_availability: Percent = None  # in Miller 2003 was 0.76
    noak: bool = None
    yearly_inflation: Percent = None
    time_to_replace: Years = None
    implosion_frequency: HZ = None  # Implosion laser driving frequency


@dataclass
class PowerTable:
    f_sub: Percent = None  # Subsystem and Control Fraction
    p_cryo: MW = None
    mn: Ratio = None  # Neutron energy multiplier
    eta_p: Percent = None  # Pumping power capture efficiency
    eta_th: Percent = None  # Thermal conversion efficiency
    fpcppf: Percent = None  # Primary Coolant Pumping Power Fraction
    p_trit: MW = None  # Tritium Systems
    p_house: MW = None  # Housekeeping power
    p_tfcool: MW = None  # Solenoid coil cooling
    p_pfcool: MW = None  # Mirror coil cooling
    p_tf: MW = None  # Power into TF coils
    p_pf: MW = None  # Power into PF (equilibrium) coils (TODO - how to handle for HTS?)
    eta_pin: Percent = None  # Input power wall plug efficiency
    eta_pin1: Percent = None
    eta_pin2: Percent = None
    eta_de: Percent = None  # Direct energy conversion efficiency
    p_input: MW = None  # Input power
    p_implosion: MW = None  # Implosion laser power
    p_ignition: MW = None  # Ignition laser power
    p_target: MW = None  # Power into target factory
    p_machinery: MW = None  # Power into machinery


@dataclass
class RadialBuild:
    # Radial build inputs
    # Radial thicknesses of concentric components (innermost to outermost)
    elon: Ratio = None  # torus elongation factor
    axis_t: Meters = None  # distance from r=0 to plasma central axis - effectively major radius
    plasma_t: Meters = None  # plasma radial thickness
    vacuum_t: Meters = None  # vacuum radial thickness
    firstwall_t: Meters = None  # first wall radial thickness
    blanket1_t: Meters = None  # blanket radial thickness
    reflector_t: Meters = None  # reflector radial thickness
    ht_shield_t: Meters = None  # High-temperature shield radial thickness
    structure_t: Meters = None  # support structure radial thickness
    gap1_t: Meters = None  # air gap radial thickness
    vessel_t: Meters = None  # vacuum vessel wall radial thickness
    coil_t: Meters = None  # TF coil radial thickness
    gap2_t: Meters = None  # second air gap radial thickness
    lt_shield_t: Meters = None  # low-temperature shield radial thickness
    bioshield_t: Meters = None  # concrete bioshield radial thickness


@dataclass
class Shield:
    # fractions
    f_SiC: Ratio = None
    FPCPPFbLi: Ratio = None
    f_W: Ratio = None
    f_BFS: Ratio = None


@dataclass
class Blanket:
    first_wall: BlanketFirstWall = None
    blanket_type: BlanketType = None
    primary_coolant: BlanketPrimaryCoolant = None
    secondary_coolant: BlanketSecondaryCoolant = None
    neutron_multiplier: BlanketNeutronMultiplier = None
    structure: BlanketStructure = None


@dataclass
class Magnet:
    name: str
    type: MagnetType
    material_type: MagnetMaterialType
    coil_count: int
    r_centre: Meters  # radius of each coil
    z_centre: Meters  # vertical coordinates of centre of each coil (r=0)
    dr: Meters  # total coil thickness in r direction (radial)
    dz: Meters  # total coil thickness in z direction (vertical)
    # Total fraction of cross-sectional area comprised of insulation
    # (for copper or tape-tape pancake geometry)
    frac_in: Ratio
    coil_temp: float  # TODO what are the units, C or K?
    mfr_factor: float  # Manufacturing factor for each coil
    # For each magnet
    # if using HTS CICC, True to autogen paramters from field and radius
    # False to use input parameters
    auto_cicc: bool = False
    # auto_cicc fields only used if auto_cicc is True
    auto_cicc_b: float = None  # central field of each autogenerated HTS CICC coil
    auto_cicc_r: Meters = None  # radius of each autogenerated HTS CICC coil
    # Structural multiplication factor.
    # This is multiplied by the magnet material cost (incl mfr factor) and added to the total
    structFactor: float = 1


@dataclass
class Coils:
    magnets: list[Magnet] = None

    struct_factor: float = 0.5  # Structural multiplication factor

    # Constants
    tape_w: Meters = 0.004  # REBCO tape width in meters
    tape_t: Meters = 0.00013  # REBCO tape thickness in meters

    # Current density of the tape in A/mm^2, set in magnetsAll function
    # approximate critical current density of YBCO at 18T
    # https://www.sciencedirect.com/science/article/pii/S0011227516303812
    j_tape_ybco: AmperesMillimeters2 = 150

    m_cost_ybco: float = 50  # Material cost of YBCO tape in $/kAm
    m_cost_ss: float = 5  # Material cost of stainless steel in $/kg
    m_cost_cu: float = 10.3  # Material cost of copper in $/kg
    # see https://cds.cern.ch/record/2839592/files/2020_04_21_SHiP_SpectrometerMagnet_Bajas.pdf
    rebco_density: float = 6350  # Density of REBCO tape in kg/m^3
    cu_density: float = 7900  # Density of copper in kg/m^3
    ss_density: float = 7900  # Density of stainless steel in kg/m^3
    mfr_factor: int = 3  # Manufacturing factor

    # Yuhu CICC HTS cable specifications
    cable_w: Meters = Meters(0.014)  # Cable width in meters
    cable_h: Meters = Meters(0.017)  # Cable height in meters
    frac_cs_cu_yuhu: float = 0.307  # Fractional cross-sectional area of copper in Yuhu Zhai's cable design
    frac_cs_ss_yuhu: float = 0.257  # Fractional cross-sectional area of stainless steel in Yuhu Zhai's cable design
    frac_cs_sc_yuhu: float = 0.257  # Fractional cross-sectional area of REBCO in Yuhu Zhai's cable design
    tot_cs_area_yuhu: Meters2 = 0.000238  # Total cross-sectional area of Yuhu Zhai's cable design in m^2

    # HTS pancake constants
    m_cost_i: float = 20  # Material cost of insulator in $/kg
    i_density: float = 3000  # Density of insulator in kg/m^3
    turns_p: float = 18  # Turns of REBCO tape per pancake
    max_cu_current: Amperes = Amperes(20)  # max current for water cooled AWG 8
    # https://www.engineeringtoolbox.com/wire-gauges-d_419.html
    cu_wire_d: float = 3.3e-3  # copper wire diameter in meters AWG8

    # COOLING 22.1.3.6
    c_frac: float = 0.1
    no_beams: Count = Count(20)  # number of beams supporting each coil, from the coil to the vessel
    beam_length: Meters = Meters(1.5)  # total length of each beam
    beam_cs_area: Meters2 = Meters2(0.25)  # cross-sectional area of each support beam
    t_op: float = 4  # operating temperature of magnets
    t_env: float = 300  # temperature of environment (to be cooled from)

    def __post_init__(self):
        if self.magnets is None:
            self.magnets = []


@dataclass
class HeatingRef:
    name: str
    type: Optional[str]
    power: MW
    cost_2009: Optional[float]
    cost_2023: float


@dataclass
class SupplementaryHeating:
    #see pg 90 https://cer.ucsd.edu/_files/publications/UCSD-CER-13-01.pdf
    nbi_power: MW = MW(50)
    icrf_power: MW = MW(0)
    aries_at: HeatingRef = HeatingRef("ARIES-AT", "ICRF/LH", MW(37.441), 1.67, 2.3881)
    aries_i_a: HeatingRef = HeatingRef("ARIES-I", "ICRF/LH", MW(96.707), 1.87, 2.6741)
    aries_i_b: HeatingRef = HeatingRef("ARIES-I'", "ICRF/LH", MW(202.5), 1.96, 2.8028)
    aries_rs: HeatingRef = HeatingRef("ARIES-RS", "ICRF/LH/HFFW", MW(80.773), 3.09, 4.4187)
    aries_iv: HeatingRef = HeatingRef("ARIES-IV", "ICRF/LH", MW(68), 4.35, 6.2205)
    aries_ii: HeatingRef = HeatingRef("ARIES-II", "ICRF/LH", MW(66.1), 4.47, 6.3921)
    # TODO why are there two ARIES-III?
    aries_iii_a: HeatingRef = HeatingRef("ARIES-III'", "NBI", MW(163.2), 4.93, 7.0499)
    aries_iii_b: HeatingRef = HeatingRef("ARIES-III", "NBI", MW(172), 4.95, 7.0785)
    iter: HeatingRef = HeatingRef("ITER", "ICRF", MW(5.5), None, 7.865)
    average: HeatingRef = HeatingRef("Average", None, MW(110.840125), 3.643333333, 5.209966667)
    average_icrf: HeatingRef = HeatingRef("Average (ICRF)", None, MW(91.92016667), 2.901666667, 4.149383333)
    average_nbi: HeatingRef = HeatingRef("Average (NBI)", None, MW(167.6), 4.94, 7.0642)

    def heating_refs(self):
        return [
            self.aries_at,
            self.aries_i_a,
            self.aries_i_b,
            self.aries_rs,
            self.aries_iv,
            self.aries_ii,
            self.aries_iii_a,
            self.aries_iii_b,
            self.iter,
            self.average,
            self.average_icrf,
            self.average_nbi,
        ]


# 22.1.5 primary structure
@dataclass
class PgaCosts():
    eng_costs: M_USD
    fab_costs: M_USD


@dataclass
class PrimaryStructure():
    # PGA stands for peak ground acceleration and increasing values would correlate to an increased risk region.
    syst_pga: StructurePga = None
    learning_credit: float = None

    analyze_costs: M_USD = 30
    unit1_seismic_costs: M_USD = 25
    reg_rev_costs: M_USD = 30
    unit1_fab_costs: M_USD = 100
    unit10_fabcosts: M_USD = 70
    pga_costs_mapping: dict[str, PgaCosts] = None

    # Dictionary of fission reactor costs from "Towards standardized nuclear reactors: Seismic isolation and the cost
    # impact of the earthquake load case" URL: https://www.sciencedirect.com/science/article/abs/pii/S0029549321004398

    def __post_init__(self):
        if self.pga_costs_mapping is None:
            self.pga_costs_mapping = {
                StructurePga.PGA_01.name: PgaCosts(eng_costs=M_USD(115), fab_costs=M_USD(115)),
                StructurePga.PGA_02.name: PgaCosts(eng_costs=M_USD(125), fab_costs=M_USD(130)),
                StructurePga.PGA_03.name: PgaCosts(eng_costs=M_USD(140), fab_costs=M_USD(165)),
                StructurePga.PGA_05.name: PgaCosts(eng_costs=M_USD(160), fab_costs=M_USD(235)),
            }

    def get_pga_costs(self) -> PgaCosts:
        return self.pga_costs_mapping[self.syst_pga.name]


# 22.1.6 Vacuum system
@dataclass
class VacuumSystem:
    # 22.1.6.1 Vacuum Vessel

    # Scaling parameters INPUTS
    learning_credit: Ratio = 0.5

    # Reference values for scaling
    # TODO confirm these units
    spool_ir: Meters = 2.25
    spool_or: Meters = 3.15
    door_irb: Meters = 6
    door_orb: Meters = 6.25
    door_irc: Meters = 7.81
    door_orc: Meters = 8.06
    spool_height: Meters = 9

    # VACUUM PUMPING 22.1.6.3
    # assume 1 second vac rate
    # cost of 1 vacuum pump, scaled from 1985 dollars
    cost_pump: float = 40000
    # 48 pumps needed for 200^3 system
    vpump_cap: float = 200 / 48  # m^3 capable of being pumped by 1 pump


@dataclass
class PowerSupplies:
    learning_credit: Unknown = 0.5
    cost_per_watt: Unknown = 1  # $1/W power supply industry rule of thumb


@dataclass
class DirectEnergyConverter:
    system_power: Unknown = 1
    flux_limit: Unknown = 2


@dataclass
class Installation:
    # 1600 dollars per day for skilled labor
    labor_rate: USD = 1600 / 1e6  # 1600 dollars per day for skilled labor
    nmod: int = 1  # number of modules


@dataclass
class FuelHandling:
    learning_curve_credit: Ratio = 0.8
    learning_tenth_of_a_kind: Ratio = None

    def __post_init__(self):
        if self.learning_tenth_of_a_kind is None:
            self.learning_tenth_of_a_kind = Ratio(10 ** (math.log10(self.learning_curve_credit) / math.log10(2)))


@dataclass
class LsaLevels:
    initialized: bool = False
    lsa: int = 2
    fac_91: list[float] = None
    fac_92: list[float] = None
    fac_93: list[float] = None
    fac_94: list[float] = None
    fac_95: list[float] = None
    fac_96: list[float] = None
    fac_97: list[float] = None
    fac_98: list[float] = None

    def __post_init__(self):
        if not self.initialized:
            # Indirect Cost Factors for different LSA levels
            self.fac_91 = [0.1130, 0.1200, 0.1280, 0.1510]  # x TDC [90]
            self.fac_92 = [0.0520, 0.0520, 0.0520, 0.0520]  # x TDC [90]
            self.fac_93 = [0.0520, 0.0600, 0.0640, 0.0870]  # x TDC [90]
            self.fac_94 = [0.1826, 0.1848, 0.1866, 0.1935]  # applies only to C90, x TDC [90+91+92+93]
            self.fac_95 = [0.0000, 0.0000, 0.0000, 0.0000]  # x TDC [90+91+92+93+94]
            self.fac_96 = [0.2050, 0.2391, 0.2565, 0.2808]  # applied only to C90, x TDC [90+91+92+93+94]
            self.fac_97 = [0.2651, 0.2736, 0.2787, 0.2915]  # applied only to C90, x TDC [90+91+92+93+94+95+96]
            self.fac_98 = [0.0000, 0.0000, 0.0000, 0.0000]  # x TDC [90+91+92+93+94+95+96]
            self.initialized = True


@dataclass
class Financial:
    # TODO what are these?
    a_c_98: Unknown = Unknown(115)
    a_power: Unknown = Unknown(1000)
    # Capital recovery factor see https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    # TODO is the capital return or recovery factor? recovery is mentioned in mfe, return in ife
    capital_recovery_factor: Ratio = 0.09


@dataclass
class Inputs(SerializableToJSON):
    # User inputs
    customer_info: CustomerInfo = field(default_factory=CustomerInfo)
    basic: Basic = field(default_factory=Basic)
    power_table: PowerTable = field(default_factory=PowerTable)
    radial_build: RadialBuild = field(default_factory=RadialBuild)
    shield: Shield = field(default_factory=Shield)
    blanket: Blanket = field(default_factory=Blanket)
    coils: Coils = field(default_factory=Coils)
    supplementary_heating: SupplementaryHeating = field(default_factory=SupplementaryHeating)
    primary_structure: PrimaryStructure = field(default_factory=PrimaryStructure)
    vacuum_system: VacuumSystem = field(default_factory=VacuumSystem)
    power_supplies: PowerSupplies = field(default_factory=PowerSupplies)
    direct_energy_converter: DirectEnergyConverter = field(default_factory=DirectEnergyConverter)
    installation: Installation = field(default_factory=Installation)
    fuel_handling: FuelHandling = field(default_factory=FuelHandling)
    lsa_levels: LsaLevels = field(default_factory=LsaLevels)
    financial: Financial = field(default_factory=Financial)

    # Library inputs
    materials: Materials = field(default_factory=Materials)
