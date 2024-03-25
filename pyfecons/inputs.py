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
    reactor_type: ReactorType = ReactorType.IFE
    energy_conversion: EnergyConversion = EnergyConversion.DIRECT
    fuel_type: FuelType = FuelType.DT
    p_nrl: MW = 2600.0
    n_mod: Count = 1
    am: Percent = 1.00
    construction_time: Years = 6.0
    plant_lifetime: Years = 30.0
    plant_availability: Percent = 0.85
    noak: bool = True
    yearly_inflation: Percent = 0.0245


@dataclass
class PowerTable:
    f_sub: Percent = 0.03
    p_cryo: MW = 0.5
    mn: Ratio = 1.1
    eta_p: Percent = 0.5
    eta_th: Percent = 0.46
    fpcppf: Percent = 0.06
    p_trit: MW = 10
    p_house: MW = 4
    p_tfcool: MW = 12.7
    p_pfcool: MW = 1
    p_tf: MW = 1
    p_pf: MW = 1
    eta_pin: Percent = 0.5
    eta_pin1: Percent = 0.18
    eta_pin2: Percent = 0.82
    eta_de: Percent = 0.85
    p_input: MW = 50


@dataclass
class RadialBuild:
    chamber_length: Meters = 40  # chamber length
    axis_t: Meters = 0  # central axis thickness
    plasma_t: Meters = 4  # Radial plasma thickness
    vacuum_t: Meters = 0.1  # Radial vacuum thickness
    firstwall_t: Meters = 0.1  # Radial firstwall thickness
    blanket1_t: Meters = 1  # Radial blanket thickness
    reflector_t: Meters = 0.1  # Radial reflector thickness
    ht_shield_t: Meters = 0.5  # Radial high temperature shield thickness
    structure_t: Meters = 0.2  # Radial structure thickness
    gap1_t: Meters = 0.5  # Radial first gap thickness
    vessel_t: Meters = 0.2  # Radial vessel wall thickness
    coil_t: Meters = 1.76  # Radial coil thickness
    gap2_t: Meters = 1  # Radial second gap thickness
    lt_shield_t: Meters = 0.3  # Radial low temperature shield thickness
    bioshield_t: Meters = 1  # Radial bioshield thickness


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
    coil_count: int
    j_cable: MA  # [MA] current
    r_centre: float
    z_centre: float
    dr: int
    dz: int


@dataclass
class Coils:
    magnets: list[Magnet] = None

    struct_factor: float = 0.5  # Structural multiplication factor

    # Constants
    cable_w: Meters = 0.014  # Cable width in meters
    cable_h: Meters = 0.017  # Cable height in meters
    tape_w: Meters = 0.004  # Tape width in meters
    tape_t: Meters = 0.00013  # Tape thickness in meters
    j_tape: AmperesMillimeters2 = 1000  # Current density of the tape in A/mm^2

    m_cost_ybco: float = 10  # Material cost of YBCO tape in $/kAm
    m_cost_ss: float = 5  # Material cost of stainless steel in $/kg
    m_cost_cu: float = 10.3  # Material cost of copper in $/kg
    cu_density: float = 7900  # Density of copper in kg/m^3
    ss_density: float = 7900  # Density of stainless steel in kg/m^3
    mfr_factor: int = 3  # Manufacturing factor

    frac_cs_cu_yuhu: float = 0.307  # Fractional cross-sectional area of copper in Yuhu Zhai's cable design
    frac_cs_ss_yuhu: float = 0.257  # Fractional cross-sectional area of stainless steel in Yuhu Zhai's cable design
    frac_cs_sc_yuhu: float = 0.257  # Fractional cross-sectional area of REBCO in Yuhu Zhai's cable design
    tot_cs_area_yuhu: Meters2 = 0.000238  # Total cross-sectional area of Yuhu Zhai's cable design in m^2

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
    nbi_power: MW = MW(25)
    icrf_power: MW = MW(25)
    aries_at: HeatingRef = None
    aries_i_a: HeatingRef = None
    aries_i_b: HeatingRef = None
    aries_rs: HeatingRef = None
    aries_iv: HeatingRef = None
    aries_ii: HeatingRef = None
    aries_iii_a: HeatingRef = None
    aries_iii_b: HeatingRef = None
    iter: HeatingRef = None
    average: HeatingRef = None
    average_icrf: HeatingRef = None
    average_nbi: HeatingRef = None

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

    def __post_init__(self):
        if self.aries_at is None:
            self.aries_at = HeatingRef("ARIES-AT", "ICRF/LH", MW(37.441), 1.67, 2.3881)
        if self.aries_i_a is None:
            self.aries_i_a = HeatingRef("ARIES-I", "ICRF/LH", MW(96.707), 1.87, 2.6741)
        if self.aries_i_b is None:
            self.aries_i_b = HeatingRef("ARIES-I'", "ICRF/LH", MW(202.5), 1.96, 2.8028)
        if self.aries_rs is None:
            self.aries_rs = HeatingRef("ARIES-RS", "LH/HFFW", MW(80.773), 3.09, 4.4187)
        if self.aries_iv is None:
            self.aries_iv = HeatingRef("ARIES-IV", "ICRF/LH", MW(68), 4.35, 6.2205)
        if self.aries_ii is None:
            self.aries_ii = HeatingRef("ARIES-II", "ICRF/LH", MW(66.1), 4.47, 6.3921)
        if self.aries_iii_a is None:
            self.aries_iii_a = HeatingRef("ARIES-III'", "NBI", MW(163.2), 4.93, 7.0499)
        if self.aries_iii_b is None:
            self.aries_iii_b = HeatingRef("ARIES-III", "NBI", MW(172), 4.95, 7.0785)
        if self.iter is None:
            self.iter = HeatingRef("ITER", "ICRF", MW(5.5), None, 7.865)
        if self.average is None:
            self.average = HeatingRef("Average", None, MW(110.840125), 3.643333333, 5.209966667)
        if self.average_icrf is None:
            self.average_icrf = HeatingRef("Average (ICRF)", None, MW(91.92016667), 2.901666667, 4.149383333)
        if self.average_nbi is None:
            self.average_nbi = HeatingRef("Average (NBI)", None, MW(167.6), 4.94, 7.0642)

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
    end_length: Meters = 8 # End parts length in meters (each)
    thickness: Meters = 0.02
    # Material properties (density and cost)
    ss_density: float = 6700  # kg/m^3
    ss_cost: float = 5  # $/kg
    vesmfr: float = 10

    # COOLING 22.1.6.2
    k_steel: float = 10
    t_mag: float = 20
    t_env: float = 300
    c_frac: float = 0.1 # cooling from power in/half carnot COP
    cop_starfire: float = 4.2 / (300 - 4.2) * 0.15 # Starfire COP
    qsci_starfire: float = 20e3 # 20 kW - STARFIRE cooling at 4.2 K
    cost_starfire: float = 17.65 * 1.43 # 17.65 M USD in 2009 for 20kW at 4.2 K, adjusted to inflation

    #VACUUM PUMPING 22.1.6.3
    #assume 1 second vac rate
    #cost of 1 vacuum pump, scaled from 1985 dollars
    cost_pump: float = 40000
    #48 pumps needed for 200^3 system
    vpump_cap: float = 200/48 #m^3 capable of beign pumped by 1 pump


@dataclass
class PowerSupplies:
    learning_credit: Unknown = 0.5


@dataclass
class DirectEnergyConverter:
    system_power: Unknown = 1
    flux_limit: Unknown = 2
    costs: dict[str, M_USD] = None

    def __post_init__(self):
        if self.costs is None:
            self.costs = {
                "EXPANDER_TANK": 16,
                "EXPANDER_COIL_AND_NEUTRON_TRAP_COIL": 33,
                "CONVERTOR_GATE_VALVE": 0.1,
                "NEUTRON_TRAP_SHIELDING": 1,
                "VACUUM_SYSTEM": 16,
                "GRID_SYSTEM": 27,
                "HEAT_COLLECTION_SYSTEM": 6,
                "ELECTRICAL_EQUIPMENT": 13,
                "COST_PER_UNIT": 112,
                "TOTAL_DEUNIT_COST": 447,
                "ENGINEERING_15_PERCENT": 67,
                "CONTINGENCY_15_PERCENT": 77,
            }


@dataclass
class Installation:
    # 1600 dollars per day for skilled labor
    labor_rate: USD = 1600 / 1e6
    r: Meters = 8  # major radius of the system
    nmod: int = 1  # number of modules


@dataclass
class FuelHandling:
    inflation: Ratio = 1.43
    learning_curve_credit: Ratio = 0.8
    learning_tenth_of_a_kind: Unknown = None

    def __post_init__(self):
        if self.learning_tenth_of_a_kind is None:
            self.learning_tenth_of_a_kind = Unknown(10 ** (math.log10(self.learning_curve_credit) / math.log10(2)))


@dataclass
class LsaLevels:
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
        if self.fac_91 is None:
            self.fac_91 = [0.1130, 0.1200, 0.1280, 0.1510]
        if self.fac_92 is None:
            self.fac_92 = [0.0520, 0.0520, 0.0520, 0.0520]
        if self.fac_93 is None:
            self.fac_93 = [0.0520, 0.0600, 0.0640, 0.0870]
        if self.fac_94 is None:
            self.fac_94 = [0.1826, 0.1848, 0.1866, 0.1935]
        if self.fac_95 is None:
            self.fac_95 = [0.0000, 0.0000, 0.0000, 0.0000]
        if self.fac_96 is None:
            self.fac_96 = [0.2050, 0.2391, 0.2565, 0.2808]
        if self.fac_97 is None:
            self.fac_97 = [0.2651, 0.2736, 0.2787, 0.2915]
        if self.fac_98 is None:
            self.fac_98 = [0.0000, 0.0000, 0.0000, 0.0000]


@dataclass
class Inputs(SerializableToJSON):
    # User inputs
    customer_info: CustomerInfo = field(default_factory=CustomerInfo)
    basic: Basic = field(default_factory=Basic)
    power_table: PowerTable = field(default_factory=PowerTable)
    radial_build: RadialBuild = field(default_factory=RadialBuild)
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

    # Library inputs
    materials: Materials = field(default_factory=Materials)
