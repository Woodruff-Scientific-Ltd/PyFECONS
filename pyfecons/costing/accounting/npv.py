from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class NPV(TemplateProvider):
    npv: M_USD = None
