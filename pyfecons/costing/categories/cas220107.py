from dataclasses import dataclass

from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS220107(ReportSection):
    # Cost Category 22.1.7 Power supplies
    C22010701: M_USD = None  # Power supplies for confinement
    C22010702: M_USD = None
    C220107: M_USD = None
