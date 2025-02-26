from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS220103Lasers(TemplateProvider):
    C220103: M_USD = None
