from pyfecons.inputs import *
from pyfecons.serializable import SerializableToJSON


# TODO give sensible defaults are force initialization
@dataclass
class PowerTable:
    p_alpha: MW = None
    p_neutron: MW = None
    p_cool: MW = None
    p_aux: MW = None
    p_coils: MW = None

    p_th: MW = None
    p_the: MW = None
    p_dee: MW = None

    p_et: MW = None
    p_loss: MW = None
    p_pump: MW = None
    p_sub: MW = None
    qsci: Unknown = None
    qeng: Unknown = None
    refrac: Unknown = None
    p_net: MW = None


# TODO give sensible defaults are force initialization
@dataclass
class CAS10:
    C110000: Currency = None
    C120000: Currency = None
    C130000: Currency = None
    C140000: Currency = None
    C150000: Currency = None
    C160000: Currency = None
    C170000: Currency = None
    C190000: Currency = None
    C100000: Currency = None


# TODO give sensible defaults are force initialization
@dataclass
class CAS21:
    C210100: Currency = None
    C210200: Currency = None
    C210300: Currency = None
    C210400: Currency = None
    C210500: Currency = None
    C210600: Currency = None
    C210700: Currency = None
    C210800: Currency = None
    C210900: Currency = None
    C211000: Currency = None
    C211100: Currency = None
    C211200: Currency = None
    C211300: Currency = None
    C211400: Currency = None
    C211500: Currency = None
    C211600: Currency = None
    C211700: Currency = None
    C211800: Currency = None
    C210000: Currency = None


# TODO give sensible defaults are force initialization
@dataclass
class CAS22:
    # Inner radii
    axis_ir: Meters = None
    plasma_ir: Meters = None
    vacuum_ir: Meters = None
    firstwall_ir: Meters = None
    blanket1_ir: Meters = None
    reflector_ir: Meters = None
    ht_shield_ir: Meters = None
    structure_ir: Meters = None
    gap1_ir: Meters = None
    vessel_ir: Meters = None
    lt_shield_ir: Meters = None  # Moved lt_shield here
    coil_ir: Meters = None  # Updated coil_ir calculation
    gap2_ir: Meters = None
    bioshield_ir: Meters = None  # Updated bioshield inner radius

    # Outer radii
    axis_or: Meters = None
    plasma_or: Meters = None
    vacuum_or: Meters = None
    firstwall_or: Meters = None
    blanket1_or: Meters = None
    reflector_or: Meters = None
    ht_shield_or: Meters = None
    structure_or: Meters = None
    gap1_or: Meters = None
    vessel_or: Meters = None
    lt_shield_or: Meters = None  # Moved lt_shield here
    coil_or: Meters = None  # Updated coil_or calculation
    gap2_or: Meters = None
    bioshield_or: Meters = None  # Updated bioshield outer radius

    # Volumes for cylinder
    axis_vol: Meters3 = None
    plasma_vol: Meters3 = None
    vacuum_vol: Meters3 = None
    firstwall_vol: Meters3 = None
    blanket1_vol: Meters3 = None
    reflector_vol: Meters3 = None
    ht_shield_vol: Meters3 = None
    structure_vol: Meters3 = None
    gap1_vol: Meters3 = None
    vessel_vol: Meters3 = None
    lt_shield_vol: Meters3 = None  # Moved lt_shield volume here
    coil_vol: Meters3 = None  # Updated coil volume calculation
    gap2_vol: Meters3 = None
    bioshield_vol: Meters3 = None  # Updated bioshield volume


@dataclass
class Data(SerializableToJSON):
    power_table = PowerTable()
    cas10 = CAS10()
    cas21 = CAS21()
    cas22 = CAS22()
