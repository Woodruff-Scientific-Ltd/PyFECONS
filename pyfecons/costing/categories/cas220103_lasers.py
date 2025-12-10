from dataclasses import dataclass

from pyfecons.units import M_USD


@dataclass
class CAS220103Lasers:
    """Cost category 22.1.3: Lasers."""

    C220103: M_USD = None  # Total cost
