from dataclasses import dataclass
from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS10(TemplateProvider):
    C110000: M_USD = None
    C120000: M_USD = None
    C130000: M_USD = None
    C140000: M_USD = None
    C150000: M_USD = None
    C160000: M_USD = None
    C170000: M_USD = None
    C190000: M_USD = None
    C100000: M_USD = None
