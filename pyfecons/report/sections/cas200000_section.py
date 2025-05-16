from dataclasses import dataclass

from pyfecons.costing.categories.cas200000 import CAS20
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS20Section(ReportSection):
    def __init__(self, cas20: CAS20):
        super().__init__()
        self.template_file = "CAS200000.tex"
        self.replacements = {
            "C200000": str(round(cas20.C200000))
        }  # TODO - not in the template
