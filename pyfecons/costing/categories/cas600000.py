from dataclasses import dataclass

from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS60(ReportSection):
    C610000: M_USD = None
    C630000LSA: M_USD = None
    C630000: M_USD = None
    C600000: M_USD = None
