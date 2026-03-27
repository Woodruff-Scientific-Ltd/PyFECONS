from dataclasses import dataclass

from pyfecons.enums import BioshieldMaterial
from pyfecons.units import Ratio


@dataclass
class Shield:
    # fractions
    f_SiC: Ratio = None
    FPCPPFbLi: Ratio = None
    f_W: Ratio = None
    f_BFS: Ratio = None

    # Bioshield safety inputs (used when safety costs enabled)
    bioshield_material: BioshieldMaterial = None
    initial_dose_without_bioshield: float = None  # Sv/yr
    regulatory_dose_limit: float = None  # Sv/yr
