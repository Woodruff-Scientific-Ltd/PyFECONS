from dataclasses import dataclass

from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS50(ReportSection):
    C510000: M_USD = None
    C520000: M_USD = None
    C530000: M_USD = None
    C540000: M_USD = None
    C550000: M_USD = None
    C580000: M_USD = None
    C590000: M_USD = None
    C500000: M_USD = None
