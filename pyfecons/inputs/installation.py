from dataclasses import dataclass

from pyfecons.units import USD


@dataclass
class Installation:
    # dollars per day for skilled labor
    labor_rate: USD = None
