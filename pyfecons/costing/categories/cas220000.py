from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS22(TemplateProvider):
    # Cost category 22.1 total
    C220100: M_USD = None

    # Final output
    C220000: M_USD = None
