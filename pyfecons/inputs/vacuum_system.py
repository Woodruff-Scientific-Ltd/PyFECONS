from dataclasses import dataclass
from pyfecons.units import Ratio, Meters, USD, Meters3, K, Meters2


# 22.1.6 Vacuum system
@dataclass
class VacuumSystem:
    # 22.1.6.1 Vacuum Vessel

    # Scaling parameters INPUTS
    learning_credit: Ratio = None

    # Reference values for scaling
    # TODO confirm these units
    spool_ir: Meters = None
    spool_or: Meters = None
    door_irb: Meters = None
    door_orb: Meters = None
    door_irc: Meters = None
    door_orc: Meters = None
    spool_height: Meters = None

    # VACUUM PUMPING 22.1.6.3
    cost_pump: USD = None
    # m^3 capable of being pumped by 1 pump
    vpump_cap: Meters3 = None

    # Temperature inputs
    # Target temperature of vacuum vessel
    t_cool: K = None
    # Temperature of environment exterior to vacuum vessel (to be pumped from)
    t_env: K = None

    # vessel construction manufacturing factor
    ves_mfr: Ratio = None

    # Support beams
    # cross-sectional area of single steel I beam, order of magnitude estimate, depends on specific beam,
    # see https://www.engineersedge.com/standard_material/Steel_ibeam_properties.htm
    beam_cs_area: Meters2 = None
    # Engineering factor of safety
    factor_of_safety: Ratio = None
    # geometry factor for uneven force distribution
    geometry_factor: Ratio = None
    # average support beam length
    beam_length: Meters = None
