from dataclasses import dataclass

from pyfecons.costing.ife.cas22.nif_costs import NifCost
from pyfecons.units import M_USD


@dataclass
class CAS220104IgnitionLasers:
    C220104: M_USD = None
    scaled_costs: dict[str, NifCost] = None
