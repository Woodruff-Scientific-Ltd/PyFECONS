from dataclasses import dataclass
from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class NPV(ReportSection):
    npv: M_USD = None
