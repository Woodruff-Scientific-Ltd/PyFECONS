from dataclasses import dataclass

from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS220108TargetFactory(ReportSection):
    C220108: M_USD = None
