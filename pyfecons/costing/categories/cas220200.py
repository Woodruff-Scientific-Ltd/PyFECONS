from dataclasses import dataclass
from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS2202(TemplateProvider):
    # MAIN AND SECONDARY COOLANT Cost Category 22.2
    C220201: M_USD = None
    C220202: M_USD = None
    C220203: M_USD = None
    C220200: M_USD = None
