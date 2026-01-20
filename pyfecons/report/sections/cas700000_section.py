from dataclasses import dataclass

from pyfecons.costing.categories.cas700000 import CAS70
from pyfecons.costing.categories.cas780000 import CAS780000
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS70Section(ReportSection):
    def __init__(self, cas70: CAS70, cas780000: CAS780000 | None = None):
        super().__init__()
        self.template_file = "CAS700000.tex"
        insurance_cost = 0 if cas780000 is None else cas780000.C780000
        self.replacements = {
            "C700000": str(round(cas70.C700000, 3)),
            "C780000": str(round(insurance_cost, 3)),
        }
