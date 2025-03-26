from dataclasses import dataclass

from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


@dataclass
class CAS2203(TemplateProvider):
    # Cost Category 22.3  Auxiliary cooling
    C220300: M_USD = None
