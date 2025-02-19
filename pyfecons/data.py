from dataclasses import dataclass, field
from typing import Union
from pyfecons.enums import MagnetType, ReactorType
from pyfecons.inputs.magnet import Magnet
from pyfecons.materials import Material
from pyfecons.serializable import SerializableToJSON
from pyfecons.units import MW, Unknown, Ratio, M_USD, Meters3, Meters2, Turns, Amperes, MA, Kilometers, \
    AmperesMillimeters2, Meters, Kilograms, Count, USD


@dataclass
class TemplateProvider:
    # template substitutions variable_name -> value
    replacements: dict[str, str] = field(default_factory=dict)
    # template file name in templates/ directory
    template_file: str = None
    # latex path -> image bytes
    figures: dict[str, bytes] = field(default_factory=dict)
    # template file path for LaTeX compilation directory (defaults to Modified/{template_file})
    _tex_path: str = None

    # TODO - tex_path is not serializing right now and I can't figure out how to get it to work
    # https://chatgpt.com/share/fab6081c-35fb-41e7-bf9a-a4e2e188865f
    @property
    def tex_path(self) -> str:
        if self._tex_path is None:
            return "Modified/" + self.template_file
        return self._tex_path

    @tex_path.setter
    def tex_path(self, value):
        self._tex_path = value


@dataclass
class PowerTable(TemplateProvider):
    p_alpha: MW = None  # Charged particle power
    p_neutron: MW = None  # Neutron power
    p_cool: MW = None
    p_aux: MW = None  # Auxiliary systems
    p_coils: MW = None
    p_th: MW = None  # Thermal power
    p_the: MW = None  # Total thermal electric power
    p_dee: MW = None
    p_et: MW = None  # Total (Gross) Electric Power
    p_loss: MW = None  # Lost Power
    p_pump: MW = None  # Primary Coolant Pumping Power
    p_sub: MW = None  # Subsystem and Control Power
    q_sci: Unknown = None  # Scientific Q
    q_eng: Unknown = None  # Engineering Q
    rec_frac: Unknown = None  # Recirculating power fraction
    p_net: MW = None  # Output Power (Net Electric Power)
    gain_e: Ratio = None  # Gain in Electric Power


# TODO give sensible defaults are force initialization
@dataclass
class CAS10(TemplateProvider):
    C110000: M_USD = None
    C120000: M_USD = None
    C130000: M_USD = None
    C140000: M_USD = None
    C150000: M_USD = None
    C160000: M_USD = None
    C170000: M_USD = None
    C190000: M_USD = None
    C100000: M_USD = None


@dataclass
class CAS21(TemplateProvider):
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
    C211900: M_USD = None
    C210000: M_USD = None


@dataclass
class MagnetProperties:
    # input
    magnet: Magnet = None

    # computed
    vol_coil: Meters3 = None  # volume of the coil
    cs_area: Meters2 = None  # cross-sectional area of entire coil
    turns_c: Turns = None  # turns of cable in the coil
    cable_current: Amperes = None  # current per cable
    current_supply: MA = None  # total current supply to the coil
    turns_sc_tot: Turns = None  # total turns of REBCO
    turns_scs: Turns = None  # turns of REBCO in one cable
    tape_length: Kilometers = None  # total length of REBCO in km
    turns_i: Turns = None  # turns of (partial?) insulation
    j_tape: AmperesMillimeters2 = None  # approximate critical current density
    cable_w: Meters = None  # Cable width in meters
    cable_h: Meters = None  # Cable height in meters
    # number of pancakes based on total required turns and the number of turns in a reference pancake coil
    no_p: float = None
    vol_i: Meters3 = None  # total volume of insulation
    max_tape_current: Amperes = None  # current
    cost_sc: M_USD = None  # total cost of REBCO
    cost_cu: M_USD = None  # total cost of copper
    cost_ss: M_USD = None  # total cost of stainless steel
    cost_i: M_USD = None  # total cost of insulation
    coil_mass: Kilograms = None  # mass of the coil
    cooling_cost: M_USD = None
    tot_mat_cost: M_USD = None
    magnet_cost: M_USD = None
    magnet_struct_cost: M_USD = None
    magnet_total_cost_individual: M_USD = None
    magnet_total_cost: M_USD = None
    cu_wire_current: Amperes = None  # current through each cu_wire


@dataclass
class CAS220101(TemplateProvider):
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

    # Volumes for torus
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
    C22010101: M_USD = None
    C22010102: M_USD = None
    C220101: M_USD = None


@dataclass
class CAS220102(TemplateProvider):
    # Cost Category 22.1.2: Shield
    C22010201: M_USD = None
    C22010202: M_USD = None
    C22010203: M_USD = None
    C22010204: M_USD = None
    C220102: M_USD = None
    V_HTS: Meters3 = None


@dataclass
class CAS220103Coils(TemplateProvider):
    # Cost Category 22.1.3: Coils
    magnet_properties: list[MagnetProperties] = None
    no_pf_coils: Count = None
    no_pf_pairs: Count = None
    total_struct_cost: M_USD = None
    C22010301: M_USD = None  # TF coils
    C22010302: M_USD = None  # CS coils
    C22010303: M_USD = None  # PF coils
    C22010304: M_USD = None  # Shim coil costs, taken as 5% total primary magnet costs
    C22010305: M_USD = None  # Structural cost
    C22010306: M_USD = None  # Cooling cost
    C220103: M_USD = None  # Total cost

    def __post_init__(self):
        if self.magnet_properties is None:
            self.magnet_properties = []

    @property
    def tf_coils(self) -> list[MagnetProperties]:
        return [
            magnet
            for magnet in self.magnet_properties
            if magnet.magnet.type == MagnetType.TF
        ]

    @property
    def cs_coils(self) -> list[MagnetProperties]:
        return [
            magnet
            for magnet in self.magnet_properties
            if magnet.magnet.type == MagnetType.CS
        ]

    @property
    def pf_coils(self) -> list[MagnetProperties]:
        return [
            magnet
            for magnet in self.magnet_properties
            if magnet.magnet.type == MagnetType.PF
        ]


@dataclass
class CAS220103Lasers(TemplateProvider):
    C220103: M_USD = None


@dataclass
class CAS220104SupplementaryHeating(TemplateProvider):
    # 22.1.4 Supplementary heating
    C22010401: M_USD = None
    C22010402: M_USD = None
    C220104: M_USD = None


@dataclass
class CAS220104IgnitionLasers(TemplateProvider):
    C220104: M_USD = None


@dataclass
class CAS220105(TemplateProvider):
    # 22.1.5 primary structure
    C22010501: M_USD = None
    C22010502: M_USD = None
    C220105: M_USD = None


@dataclass
class VesselCost:
    name: str = None
    total_mass: Kilograms = 0
    material_cost: USD = 0
    fabrication_cost: USD = 0
    total_cost: USD = 0


@dataclass
class VesselCosts:
    spool_assembly: VesselCost = field(default_factory=VesselCost)
    removable_doors: VesselCost = field(default_factory=VesselCost)
    door_frames: VesselCost = field(default_factory=VesselCost)
    port_enclosures: VesselCost = field(default_factory=VesselCost)
    total: VesselCost = field(default_factory=VesselCost)
    contingency: VesselCost = field(default_factory=VesselCost)
    prime_contractor_fee: VesselCost = field(default_factory=VesselCost)
    total_subsystem_cost: VesselCost = field(default_factory=VesselCost)


@dataclass
class CAS220106(TemplateProvider):
    # 22.1.6 Vacuum system
    C22010601: M_USD = None
    C22010602: M_USD = None
    C22010603: M_USD = None
    C22010604: M_USD = None
    C220106: M_USD = None
    massstruct: float = None
    vesvol: float = None
    vesmatcost: float = None
    vessel_costs: VesselCosts = field(default_factory=VesselCosts)


@dataclass
class CAS220107(TemplateProvider):
    # Cost Category 22.1.7 Power supplies
    C22010701: M_USD = None  # Power supplies for confinement
    C22010702: M_USD = None
    C220107: M_USD = None


@dataclass
class CAS220108Divertor(TemplateProvider):
    # 22.1.8 Divertor
    C220108: M_USD = None
    divertor_maj_rad: Meters = None
    divertor_min_rad: Meters = None
    divertor_thickness_z: Meters = None
    divertor_complexity_factor: Ratio = (
        None  # arbitrary measure of how complicated the divertor design is
    )
    divertor_vol_frac: Ratio = None  # fraction of volume of divertor that is material
    divertor_thickness_r: Meters = None
    divertor_material: Material = None
    divertor_vol: Meters3 = None  # volume of the divertor based on TF coil radius
    divertor_mass: Kilograms = None
    divertor_mat_cost: M_USD = None
    divertor_cost: M_USD = None


@dataclass
class CAS220108TargetFactory(TemplateProvider):
    C220108: M_USD = None


@dataclass
class CAS220109(TemplateProvider):
    # 22.1.9 Direct Energy Converter
    C220109: M_USD = None
    costs: dict[str, M_USD] = None
    scaled_costs: dict[str, M_USD] = None


@dataclass
class CAS220111(TemplateProvider):
    # Cost Category 22.1.11 Installation costs
    C220111: M_USD = None


@dataclass
class CAS220119(TemplateProvider):
    # Cost category 22.1.19 Scheduled Replacement Cost
    C220119: M_USD = None


@dataclass
class CAS2202(TemplateProvider):
    # MAIN AND SECONDARY COOLANT Cost Category 22.2
    C220201: M_USD = None
    C220202: M_USD = None
    C220203: M_USD = None
    C220200: M_USD = None


@dataclass
class CAS2203(TemplateProvider):
    # Cost Category 22.3  Auxiliary cooling
    C220300: M_USD = None


@dataclass
class CAS2204(TemplateProvider):
    # Cost Category 22.4 Radwaste
    C220400: M_USD = None


@dataclass
class CAS2205(TemplateProvider):
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


@dataclass
class CAS2206(TemplateProvider):
    # Cost Category 22.6 Other Reactor Plant Equipment
    C220600: M_USD = None


@dataclass
class CAS2207(TemplateProvider):
    # Cost Category 22.7 Instrumentation and Control
    C220700: M_USD = None


@dataclass
class CAS22(TemplateProvider):
    # Cost category 22.1 total
    C220100: M_USD = None

    # Final output
    C220000: M_USD = None


@dataclass
class CAS23(TemplateProvider):
    C230000: M_USD = None


@dataclass
class CAS24(TemplateProvider):
    C240000: M_USD = None


@dataclass
class CAS25(TemplateProvider):
    C250000: M_USD = None


@dataclass
class CAS26(TemplateProvider):
    C260000: M_USD = None


@dataclass
class CAS27(TemplateProvider):
    C271000: M_USD = None
    C274000: M_USD = None
    C275000: M_USD = None
    C270000: M_USD = None


@dataclass
class CAS28(TemplateProvider):
    C280000: M_USD = None


@dataclass
class CAS29(TemplateProvider):
    C290000: M_USD = None


@dataclass
class CAS20(TemplateProvider):
    C200000: M_USD = None


@dataclass
class CAS30(TemplateProvider):
    C310000LSA: M_USD = None
    C310000: M_USD = None
    C320000LSA: M_USD = None
    C320000: M_USD = None
    C350000LSA: M_USD = None
    C350000: M_USD = None
    C300000: M_USD = None


@dataclass
class CAS40(TemplateProvider):
    C400000LSA: M_USD = None
    C400000: M_USD = None
    C410000: M_USD = None
    C420000: M_USD = None
    C430000: M_USD = None
    C440000: M_USD = None


@dataclass
class CAS50(TemplateProvider):
    C510000: M_USD = None
    C520000: M_USD = None
    C530000: M_USD = None
    C540000: M_USD = None
    C550000: M_USD = None
    C580000: M_USD = None
    C590000: M_USD = None
    C500000: M_USD = None


@dataclass
class CAS60(TemplateProvider):
    C610000: M_USD = None
    C630000LSA: M_USD = None
    C630000: M_USD = None
    C600000: M_USD = None


@dataclass
class CAS70(TemplateProvider):
    C700000: M_USD = None


@dataclass
class CAS80(TemplateProvider):
    C800000: M_USD = None


@dataclass
class CAS90(TemplateProvider):
    C990000: M_USD = None
    C900000: M_USD = None


@dataclass
class LCOE(TemplateProvider):
    C1000000: M_USD = None
    C2000000: M_USD = None


@dataclass
class CostTable(TemplateProvider):
    pass


@dataclass
class NPV(TemplateProvider):
    npv: M_USD = None


@dataclass
class Data(SerializableToJSON):
    reactor_type: ReactorType
    power_table: PowerTable = field(default_factory=PowerTable)
    cas10: CAS10 = field(default_factory=CAS10)
    cas21: CAS21 = field(default_factory=CAS21)
    cas22: CAS22 = field(default_factory=CAS22)
    cas220101: CAS220101 = field(default_factory=CAS220101)
    cas220102: CAS220102 = field(default_factory=CAS220102)
    cas220103: Union[CAS220103Coils, CAS220103Lasers] = field(default=None)
    cas220104: Union[CAS220104SupplementaryHeating, CAS220104IgnitionLasers] = field(
        default=None
    )
    cas220105: CAS220105 = field(default_factory=CAS220105)
    cas220106: CAS220106 = field(default_factory=CAS220106)
    cas220107: CAS220107 = field(default_factory=CAS220107)
    cas220108: Union[CAS220108Divertor, CAS220108TargetFactory] = field(default=None)
    cas220109: CAS220109 = field(default_factory=CAS220109)
    cas220111: CAS220111 = field(default_factory=CAS220111)
    cas220119: CAS220119 = field(default_factory=CAS220119)
    cas2202: CAS2202 = field(default_factory=CAS2202)
    cas2203: CAS2203 = field(default_factory=CAS2203)
    cas2204: CAS2204 = field(default_factory=CAS2204)
    cas2205: CAS2205 = field(default_factory=CAS2205)
    cas2206: CAS2206 = field(default_factory=CAS2206)
    cas2207: CAS2207 = field(default_factory=CAS2207)
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
    cas90: CAS90 = field(default_factory=CAS90)
    lcoe: LCOE = field(default_factory=LCOE)
    cost_table: CostTable = field(default_factory=CostTable)
    npv: NPV = field(default_factory=NPV)

    def __post_init__(self):
        if self.cas220103 is None:
            self.cas220103 = self._initialize_cas220103()
        if self.cas220104 is None:
            self.cas220104 = self._initialize_cas220104()
        if self.cas220108 is None:
            self.cas220108 = self._initialize_cas220108()

    def _initialize_cas220103(self) -> Union[CAS220103Coils, CAS220103Lasers]:
        if self.reactor_type == ReactorType.MFE:
            return CAS220103Coils()
        elif self.reactor_type == ReactorType.IFE:
            return CAS220103Lasers()
        else:  # mif
            raise ValueError("Invalid reactor type. 'mif' is not yet supported.")

    def _initialize_cas220104(
        self,
    ) -> Union[CAS220104SupplementaryHeating, CAS220104IgnitionLasers]:
        if self.reactor_type == ReactorType.MFE:
            return CAS220104SupplementaryHeating()
        elif self.reactor_type == ReactorType.IFE:
            return CAS220104IgnitionLasers()
        else:  # mif
            raise ValueError("Invalid reactor type. 'mif' is not yet supported.")

    def _initialize_cas220108(self) -> Union[CAS220108Divertor, CAS220108TargetFactory]:
        if self.reactor_type == ReactorType.MFE:
            return CAS220108Divertor()
        elif self.reactor_type == ReactorType.IFE:
            return CAS220108TargetFactory()
        else:  # mif
            raise ValueError("Invalid reactor type. 'mif' is not yet supported.")
