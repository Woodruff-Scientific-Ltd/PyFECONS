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
    j_cable: MA   # [MA] current
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
    aries_at: HeatingRef = field(default=HeatingRef("ARIES-AT", "ICRF/LH", MW(37.441), 1.67, 2.3881))
    aries_i_a: HeatingRef = field(default=HeatingRef("ARIES-I", "ICRF/LH", MW(96.707), 1.87, 2.6741))
    aries_i_b: HeatingRef = field(default=HeatingRef("ARIES-I'", "ICRF/LH", MW(202.5), 1.96, 2.8028))
    aries_rs: HeatingRef = field(default=HeatingRef("ARIES-RS", "LH/HFFW", MW(80.773), 3.09, 4.4187))
    aries_iv: HeatingRef = field(default=HeatingRef("ARIES-IV", "ICRF/LH", MW(68), 4.35, 6.2205))
    aries_ii: HeatingRef = field(default=HeatingRef("ARIES-II", "ICRF/LH", MW(66.1), 4.47, 6.3921))
    aries_iii_a: HeatingRef = field(default=HeatingRef("ARIES-III'", "NBI", MW(163.2), 4.93, 7.0499))
    aries_iii_b: HeatingRef = field(default=HeatingRef("ARIES-III", "NBI", MW(172), 4.95, 7.0785))
    iter: HeatingRef = field(default=HeatingRef("ITER", "ICRF", MW(5.5), None, 7.865))
    average: HeatingRef = field(default=HeatingRef("Average", None, MW(110.840125), 3.643333333, 5.209966667))
    average_icrf: HeatingRef = field(default=HeatingRef("Average (ICRF)", None, MW(91.92016667), 2.901666667, 4.149383333))
    average_nbi: HeatingRef = field(default=HeatingRef("Average (NBI)", None, MW(167.6), 4.94, 7.0642))

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

    # Library inputs
    materials: Materials = field(default_factory=Materials)
