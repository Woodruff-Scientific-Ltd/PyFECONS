from dataclasses import dataclass
from typing import Optional

from pyfecons.units import MW


@dataclass
class HeatingRef:
    name: str
    type: Optional[str]
    power: MW
    cost_2009: Optional[float]
    cost_2023: float
