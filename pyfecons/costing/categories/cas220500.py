from dataclasses import dataclass

from pyfecons.report import ReportSection
from pyfecons.units import M_USD


@dataclass
class CAS2205(ReportSection):
    # Cost Category 22.5 Fuel Handling and Storage
    C2205010ITER: M_USD = None
    C2205020ITER: M_USD = None
    C2205030ITER: M_USD = None
    C2205040ITER: M_USD = None
    C2205050ITER: M_USD = None
    C2205060ITER: M_USD = None
    C22050ITER: M_USD = None
    C220501: M_USD = None
    C220502: M_USD = None
    C220503: M_USD = None
    C220504: M_USD = None
    C220505: M_USD = None
    C220506: M_USD = None
    C220500: M_USD = None
