from dataclasses import dataclass

from pyfecons.enums import (
    BlanketFirstWall,
    BlanketType,
    BlanketPrimaryCoolant,
    BlanketSecondaryCoolant,
    BlanketNeutronMultiplier,
    BlanketStructure,
)


@dataclass
class Blanket:
    first_wall: BlanketFirstWall = None
    blanket_type: BlanketType = None
    primary_coolant: BlanketPrimaryCoolant = None
    secondary_coolant: BlanketSecondaryCoolant = None
    neutron_multiplier: BlanketNeutronMultiplier = None
    structure: BlanketStructure = None
