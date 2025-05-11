from dataclasses import dataclass

from pyfecons.costing.categories.cas260000 import CAS26
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS26Section(ReportSection):
    def __init__(self, cas26: CAS26):
        super().__init__()
        self.template_file = "CAS260000.tex"
        self.replacements = {"C260000": round(cas26.C260000, 1)}