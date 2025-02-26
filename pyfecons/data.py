from dataclasses import dataclass, field
from typing import Union

from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.categories.cas10 import CAS10
from pyfecons.costing.categories.cas21 import CAS21
from pyfecons.costing.categories.cas220101 import CAS220101
from pyfecons.costing.categories.cas220102 import CAS220102
from pyfecons.costing.categories.cas220103_coils import CAS220103Coils
from pyfecons.costing.categories.cas220103_lasers import CAS220103Lasers
from pyfecons.costing.categories.cas220104_ignition_lasers import (
    CAS220104IgnitionLasers,
)
from pyfecons.costing.categories.cas220104_supplementary_heating import (
    CAS220104SupplementaryHeating,
)
from pyfecons.costing.categories.cas220105 import CAS220105
from pyfecons.enums import ReactorType
from pyfecons.materials import Material
from pyfecons.report import TemplateProvider
from pyfecons.serializable import SerializableToJSON
from pyfecons.units import Ratio, M_USD, Meters3, Meters, Kilograms, USD


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

    def template_providers(self) -> list[TemplateProvider]:
        return [
            self.power_table,
            self.cas10,
            self.cas21,
            self.cas220101,
            self.cas220102,
            self.cas220103,
            self.cas220104,
            self.cas220105,
            self.cas220106,
            self.cas220107,
            self.cas220108,
            self.cas220109,
            self.cas220111,
            self.cas220119,
            self.cas2202,
            self.cas2203,
            self.cas2204,
            self.cas2205,
            self.cas2206,
            self.cas2207,
            self.cas22,
            self.cas23,
            self.cas24,
            self.cas25,
            self.cas26,
            self.cas27,
            self.cas28,
            self.cas29,
            self.cas20,
            self.cas30,
            self.cas40,
            self.cas50,
            self.cas60,
            self.cas70,
            self.cas80,
            self.cas90,
            self.lcoe,
            self.cost_table,
            self.npv,
        ]
