from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS28(TemplateProvider):
    C280000: M_USD = None
