from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS220109(TemplateProvider):
    # 22.1.9 Direct Energy Converter
    C220109: M_USD = None
    costs: dict[str, M_USD] = None
    scaled_costs: dict[str, M_USD] = None
