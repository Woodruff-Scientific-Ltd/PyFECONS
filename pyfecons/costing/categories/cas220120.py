from dataclasses import dataclass

from pyfecons.units import M_USD


@dataclass
class CAS220120:
    """Cost Category 22.01.20: Disruption Mitigation System

    This category includes the cost of the shattered pellet injection system
    used to mitigate plasma disruption effects in tokamak fusion reactors.
    """

    C220120: M_USD = None
