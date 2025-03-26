from dataclasses import dataclass

from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS22(ReportSection):
    # Cost category 22.1 total
    C220100: M_USD = None

    # Final output
    C220000: M_USD = None
