from dataclasses import dataclass

from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS2207(ReportSection):
    # Cost Category 22.7 Instrumentation and Control
    C220700: M_USD = None
