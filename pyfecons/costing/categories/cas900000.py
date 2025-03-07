from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS90(TemplateProvider):
    C990000: M_USD = None
    C900000: M_USD = None
