from dataclasses import dataclass

from pyfecons.costing.models.magnet_properties import MagnetProperties
from pyfecons.enums import MagnetType
from pyfecons.units import Count, M_USD


@dataclass
class CAS220103Coils:
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
