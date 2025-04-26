from dataclasses import dataclass

from pyfecons.costing.categories.cas220109 import CAS220109
from pyfecons.report.section import ReportSection


@dataclass
class CAS220109Section(ReportSection):
    def __init__(self, cas220109: CAS220109):
        super().__init__()
        self.template_file = "CAS220109.tex"
        self.replacements = self.get_replacements(cas220109)

    def get_replacements(self, cas220109: CAS220109) -> dict[str, str]:
        replacements = {
            key: str(round(value, 1)) for key, value in cas220109.scaled_costs.items()
        }
        replacements["totaldecost"] = str(
            round(sum(cas220109.scaled_costs.values()), 1)
        )
        replacements["C220109"] = str(cas220109.C220109)
        return replacements
