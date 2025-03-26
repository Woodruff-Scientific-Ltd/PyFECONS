from dataclasses import dataclass

from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS220104IgnitionLasers(ReportSection):
    C220104: M_USD = None
