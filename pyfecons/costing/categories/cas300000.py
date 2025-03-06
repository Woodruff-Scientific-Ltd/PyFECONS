from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS30(TemplateProvider):
    C310000LSA: M_USD = None
    C310000: M_USD = None
    C320000LSA: M_USD = None
    C320000: M_USD = None
    C350000LSA: M_USD = None
    C350000: M_USD = None
    C300000: M_USD = None
