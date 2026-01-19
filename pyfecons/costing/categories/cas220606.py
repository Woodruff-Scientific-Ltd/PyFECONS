from dataclasses import dataclass

from pyfecons.units import M_USD


@dataclass
class CAS220606:
    # Cost Category 22.06.06 Remote Handling equipment
    C220606: M_USD = None
