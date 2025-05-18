from dataclasses import dataclass

from pyfecons.units import M_USD


@dataclass
class CAS2204:
    # Cost Category 22.4 Radwaste
    C220400: M_USD = None
