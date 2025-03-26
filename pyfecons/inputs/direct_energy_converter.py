from dataclasses import dataclass

from pyfecons.units import Unknown


@dataclass
class DirectEnergyConverter:
    system_power: Unknown = None
    flux_limit: Unknown = None
