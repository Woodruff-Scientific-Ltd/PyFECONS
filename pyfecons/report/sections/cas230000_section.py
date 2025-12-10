from dataclasses import dataclass

from pyfecons.costing.categories.cas230000 import CAS23
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS23Section(ReportSection):
    def __init__(self, cas23: CAS23):
        super().__init__()
        self.template_file = "CAS230000.tex"
        self.replacements = {"C230000": str(round(cas23.C230000, 1))}
