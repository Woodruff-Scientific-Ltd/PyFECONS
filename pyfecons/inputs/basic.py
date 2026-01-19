from dataclasses import dataclass

from pyfecons.enums import (
    ConfinementType,
    EnergyConversion,
    FuelType,
    FusionMachineType,
    Region,
)
from pyfecons.units import HZ, MW, Count, Percent, Years


@dataclass
class Basic:
    fusion_machine_type: FusionMachineType = None
    confinement_type: ConfinementType = None
    energy_conversion: EnergyConversion = None
    fuel_type: FuelType = FuelType.DT
    p_nrl: MW = None  # Fusion Power
    n_mod: Count = None
    am: Percent = None
    downtime: Years = None
    construction_time: Years = None
    plant_lifetime: Years = None  # from end of construction
    plant_availability: Percent = None  # in Miller 2003 was 0.76
    noak: bool = None
    yearly_inflation: Percent = None
    time_to_replace: Years = None
    implosion_frequency: HZ = None  # Implosion laser driving frequency
    include_safety_hazards_costs: bool = (
        False  # Include safety and hazard mitigation costs
    )
    region: Region = Region.UNSPECIFIED
