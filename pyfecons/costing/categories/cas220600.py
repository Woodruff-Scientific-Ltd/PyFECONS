from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS2206(TemplateProvider):
    # Cost Category 22.6 Other Reactor Plant Equipment
    C220600: M_USD = None
