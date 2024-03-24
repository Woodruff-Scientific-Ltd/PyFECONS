from pyfecons.inputs import *
from pyfecons.materials import Material
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
    recfrac: Unknown = None
    p_net: MW = None


# TODO give sensible defaults are force initialization
@dataclass
class CAS10:
    C110000: M_USD = None
    C120000: M_USD = None
    C130000: M_USD = None
    C140000: M_USD = None
    C150000: M_USD = None
    C160000: M_USD = None
    C170000: M_USD = None
    C190000: M_USD = None
    C100000: M_USD = None


# TODO give sensible defaults are force initialization
@dataclass
class CAS21:
    C210100: M_USD = None
    C210200: M_USD = None
    C210300: M_USD = None
    C210400: M_USD = None
    C210500: M_USD = None
    C210600: M_USD = None
    C210700: M_USD = None
    C210800: M_USD = None
    C210900: M_USD = None
    C211000: M_USD = None
    C211100: M_USD = None
    C211200: M_USD = None
    C211300: M_USD = None
    C211400: M_USD = None
    C211500: M_USD = None
    C211600: M_USD = None
    C211700: M_USD = None
    C211800: M_USD = None
    C210000: M_USD = None


@dataclass
class MagnetProperties:
    # input
    magnet: Magnet

    # computed
    vol_coil: Meters3 = None
    cs_area: Meters2 = None
    turns_c: Turns = None
    cable_current: Amperes = None  # TODO - currently not used in template, should it be?
    current_supply: MA = None
    turns_sc_tot: Turns = None
    tape_length: Kilometers = None
    tape_current: Amperes = None
    cost_sc: M_USD = None
    cost_cu: M_USD = None
    cost_ss: M_USD = None
    tot_mat_cost: M_USD = None
    magnet_cost: M_USD = None
    magnet_struct_cost: M_USD = None
    magnet_total_cost_individual: M_USD = None
    magnet_total_cost: M_USD = None


# TODO give sensible defaults are force initialization
# TODO group inputs by section into classes
@dataclass
class CAS22:
    # Cost Category 22.1.1: Reactor Equipment
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

    # Costs
    C220101: M_USD = None

    # Cost Category 22.1.2: Shield
    C22010201: M_USD = None
    C22010202: M_USD = None
    C22010203: M_USD = None
    C22010204: M_USD = None
    C220102: M_USD = None
    V_HTS: Meters3 = None

    # Cost Category 22.1.3: Coils
    magnet_properties: list[MagnetProperties] = None
    total_struct_cost: M_USD = None
    C22010301: M_USD = None  # Assuming mag cost is for the first type of coils
    C22010302: M_USD = None  # Sum of costs for other types of coils
    C22010303: M_USD = None  # Additional costs
    C22010304: M_USD = None  # Structural cost
    C220103: M_USD = None  # Total cost

    # 22.1.4 Supplementary heating
    C22010401: M_USD = None
    C22010402: M_USD = None
    C220104: M_USD = None

    # 22.1.5 primary structure
    C22010501: M_USD = None
    C22010502: M_USD = None
    C220105: M_USD = None

    # 22.1.6 Vacuum system
    C22010601: M_USD = None
    C22010602: M_USD = None
    C22010603: M_USD = None
    C22010604: M_USD = None
    C220106: M_USD = None
    vesvol: float = None
    materialvolume: float = None
    massstruct: float = None
    vesmatcost: float = None
    q_in: float = None

    # Cost Category 22.1.7 Power supplies
    C220107: M_USD = None

    # 22.1.8 Divertor
    C220108: M_USD = None
    divertor_maj_rad: Meters = None
    divertor_min_rad: Meters = None
    divertor_thickness_z: Meters = None
    divertor_thickness_r: Meters = None
    divertor_material: Material = None
    divertor_vol: Meters3 = None
    divertor_mass: Kilograms = None
    divertor_mat_cost: M_USD = None
    divertor_cost: M_USD = None

    # 22.1.9 Direct Energy Converter
    C220109: M_USD = None
    scaled_direct_energy_costs: dict[str, M_USD] = None

    # Cost Category 22.1.11 Installation costs
    C220111: M_USD = None

    # Cost category 22.1.19 Scheduled Replacement Cost
    C220119: M_USD = None

    # Cost category 22.1 total
    C220100: M_USD = None

    # MAIN AND SECONDARY COOLANT Cost Category 22.2
    C220201: M_USD = None
    C220202: M_USD = None
    C220203: M_USD = None
    C220200: M_USD = None

    # Cost Category 22.3  Auxiliary cooling
    C220300: M_USD = None

    # Cost Category 22.4 Radwaste
    C220400: M_USD = None

    # Cost Category 22.5 Fuel Handling and Storage
    C2205010ITER: M_USD = None
    C2205020ITER: M_USD = None
    C2205030ITER: M_USD = None
    C2205040ITER: M_USD = None
    C2205050ITER: M_USD = None
    C2205060ITER: M_USD = None
    C22050ITER: M_USD = None
    C220501: M_USD = None
    C220502: M_USD = None
    C220503: M_USD = None
    C220504: M_USD = None
    C220505: M_USD = None
    C220506: M_USD = None
    C220500: M_USD = None

    # Cost Category 22.6 Other Reactor Plant Equipment
    C220600: M_USD = None

    # Cost Category 22.7 Instrumentation and Control
    C220700: M_USD = 85

    # Final output
    C220000: M_USD = None

    def __post_init__(self):
        if self.magnet_properties is None:
            self.magnet_properties = []


@dataclass
class CAS23:
    C230000: M_USD = None


@dataclass
class CAS24:
    C240000: M_USD = None


@dataclass
class CAS25:
    C250000: M_USD = None


@dataclass
class CAS26:
    C260000: M_USD = None


@dataclass
class CAS27:
    C271000: M_USD = None
    C274000: M_USD = None
    C275000: M_USD = None
    C270000: M_USD = None


@dataclass
class CAS28:
    C280000: M_USD = None


@dataclass
class CAS29:
    C290000: M_USD = None


@dataclass
class CAS20:
    C200000: M_USD = None


@dataclass
class CAS30:
    C310000LSA: M_USD = None
    C310000: M_USD = None
    C320000LSA: M_USD = None
    C320000: M_USD = None
    C350000LSA: M_USD = None
    C350000: M_USD = None
    C300000: M_USD = None


@dataclass
class CAS40:
    C400000LSA : M_USD = None
    C400000 : M_USD = None


@dataclass
class CAS50:
    C510000: M_USD = None
    C520000: M_USD = None
    C530000: M_USD = None
    C540000: M_USD = None
    C550000: M_USD = None
    C580000: M_USD = None
    C590000: M_USD = None
    C500000: M_USD = None


@dataclass
class CAS60:
    C610000: M_USD = None
    C630000LSA: M_USD = None
    C630000: M_USD = None
    C600000: M_USD = None


@dataclass
class CAS70:
    C700000: M_USD = None


@dataclass
class CAS80:
    C800000: M_USD = None


@dataclass
class Data(SerializableToJSON):
    power_table: PowerTable = field(default_factory=PowerTable)
    cas10: CAS10 = field(default_factory=CAS10)
    cas21: CAS21 = field(default_factory=CAS21)
    cas22: CAS22 = field(default_factory=CAS22)
    cas23: CAS23 = field(default_factory=CAS23)
    cas24: CAS24 = field(default_factory=CAS24)
    cas25: CAS25 = field(default_factory=CAS25)
    cas26: CAS26 = field(default_factory=CAS26)
    cas27: CAS27 = field(default_factory=CAS27)
    cas28: CAS28 = field(default_factory=CAS28)
    cas29: CAS29 = field(default_factory=CAS29)
    cas20: CAS20 = field(default_factory=CAS20)
    cas30: CAS30 = field(default_factory=CAS30)
    cas40: CAS40 = field(default_factory=CAS40)
    cas50: CAS50 = field(default_factory=CAS50)
    cas60: CAS60 = field(default_factory=CAS60)
    cas70: CAS70 = field(default_factory=CAS70)
    cas80: CAS80 = field(default_factory=CAS80)
