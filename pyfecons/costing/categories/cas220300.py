from dataclasses import dataclass

from pyfecons.units import M_USD


@dataclass
class CAS2203:
    # Cost Category 22.3  Auxiliary cooling
    C220300: M_USD = None
