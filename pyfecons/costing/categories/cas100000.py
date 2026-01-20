from dataclasses import dataclass

from pyfecons.units import M_USD


@dataclass
class CAS10:
    """Cost Category 10: Pre-construction Costs"""

    # Cost Category 11 – Land and Land Rights
    # C110100: baseline land and land rights (power-based site cost)
    # C110200: safety-driven land and mitigation add-on (e.g., tritium release)
    C110100: M_USD = None
    C110200: M_USD = None
    C110000: M_USD = None
    C120000: M_USD = None
    C130000: M_USD = None
    C140000: M_USD = None
    C150000: M_USD = None
    C160000: M_USD = None
    C170000: M_USD = None
    C190000: M_USD = None
    C100000: M_USD = None
