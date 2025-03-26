from dataclasses import dataclass
from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS220105(ReportSection):
    # 22.1.5 primary structure
    C22010501: M_USD = None
    C22010502: M_USD = None
    C220105: M_USD = None
