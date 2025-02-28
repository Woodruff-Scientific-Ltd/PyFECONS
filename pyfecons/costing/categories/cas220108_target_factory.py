from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS220108TargetFactory(TemplateProvider):
    C220108: M_USD = None
