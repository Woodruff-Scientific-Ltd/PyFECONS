from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS220104SupplementaryHeating(TemplateProvider):
    # 22.1.4 Supplementary heating
    C22010401: M_USD = None
    C22010402: M_USD = None
    C220104: M_USD = None
