from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class LCOE(TemplateProvider):
    C1000000: M_USD = None
    C2000000: M_USD = None
