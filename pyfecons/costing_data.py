from dataclasses import dataclass

from pyfecons.data import Data
from pyfecons.report import TemplateProvider


@dataclass
class CostingData:
    data: Data = None
    template_providers: list[TemplateProvider] = None

    def __post_init__(self):
        if self.template_providers is None:
            self.template_providers = []
