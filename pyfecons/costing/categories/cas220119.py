from dataclasses import dataclass

from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS220119(ReportSection):
    # Cost category 22.1.19 Scheduled Replacement Cost
    C220119: M_USD = None
