from dataclasses import dataclass
from typing import Dict

from pyfecons.costing.models.target_factory_cost import TargetFactoryCost
from pyfecons.units import M_USD


@dataclass
class CAS220108TargetFactory:
    C220108: M_USD = None
    target_factory_costs: Dict[str, TargetFactoryCost] = None
