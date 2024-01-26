from dataclasses import dataclass, field
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
class Inputs(SerializableToJSON):
    # User inputs
    customer_info: CustomerInfo = field(default_factory=CustomerInfo)
    basic: Basic = field(default_factory=Basic)
    power_table: PowerTable = field(default_factory=PowerTable)
    radial_build: RadialBuild = field(default_factory=RadialBuild)
    blanket: Blanket = field(default_factory=Blanket)

    # Library inputs
    materials: Materials = field(default_factory=Materials)
