from dataclasses import dataclass

from pyfecons.units import M_USD, Meters, Meters3


@dataclass
class CAS220102:
    # Cost Category 22.1.2: Shield
    C22010201: M_USD = None
    C22010202: M_USD = None
    C22010203: M_USD = None
    C22010204: M_USD = None
    C220102: M_USD = None
    V_HTS: Meters3 = None

    # Dose-based bioshield outputs (populated when safety enabled)
    bioshield_required_thickness: Meters = None
    bioshield_dose_dtf: float = None
    bioshield_material_name: str = None
    bioshield_vol_safety: Meters3 = None
