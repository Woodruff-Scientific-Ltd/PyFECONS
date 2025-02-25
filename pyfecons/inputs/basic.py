from dataclasses import dataclass

from pyfecons.enums import ReactorType, ConfinementType, EnergyConversion, FuelType
from pyfecons.units import MW, Count, Percent, Years, HZ


@dataclass
class Basic:
    reactor_type: ReactorType = None
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
