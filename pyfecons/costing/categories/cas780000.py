from dataclasses import dataclass

from pyfecons.units import M_USD


@dataclass
class CAS780000:
    # Cost Category 78 – Taxes and Insurance (insurance component)
    C780000: M_USD = None
