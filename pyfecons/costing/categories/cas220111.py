from dataclasses import dataclass

from pyfecons.units import M_USD


@dataclass
class CAS220111:
    # Cost Category 22.1.11 Installation costs
    C220111: M_USD = None
