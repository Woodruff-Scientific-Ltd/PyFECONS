from dataclasses import dataclass

from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS40(ReportSection):
    C400000LSA: M_USD = None
    C400000: M_USD = None
    C410000: M_USD = None
    C420000: M_USD = None
    C430000: M_USD = None
    C440000: M_USD = None
