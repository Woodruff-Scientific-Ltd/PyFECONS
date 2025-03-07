from dataclasses import dataclass

from pyfecons.report import TemplateProvider


# TODO - this is not actually a cost calculation and should go in a report section
@dataclass
class CostTable(TemplateProvider):
    pass
