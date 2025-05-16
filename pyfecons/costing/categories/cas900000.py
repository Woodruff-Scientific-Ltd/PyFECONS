from dataclasses import dataclass
from pyfecons.units import M_USD


@dataclass
class CAS90:
    C990000: M_USD = None
    C900000: M_USD = None
