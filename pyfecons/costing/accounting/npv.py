from dataclasses import dataclass

from pyfecons.units import M_USD


@dataclass
class NPV:
    npv: M_USD = None
