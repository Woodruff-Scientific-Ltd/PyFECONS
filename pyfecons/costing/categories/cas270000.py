from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS27(TemplateProvider):
    C271000: M_USD = None
    C274000: M_USD = None
    C275000: M_USD = None
    C270000: M_USD = None
