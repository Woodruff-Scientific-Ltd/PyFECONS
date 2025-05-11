from dataclasses import dataclass

from pyfecons.costing.categories.cas250000 import CAS25
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS25Section(ReportSection):
    def __init__(self, cas25: CAS25):
        super().__init__()
        self.template_file = "CAS250000.tex"
        self.replacements = {"C250000": round(cas25.C250000, 1)}
