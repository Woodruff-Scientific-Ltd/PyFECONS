from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS220104IgnitionLasers(TemplateProvider):
    C220104: M_USD = None
