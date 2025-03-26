from dataclasses import dataclass

from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS220103Lasers(ReportSection):
    C220103: M_USD = None
