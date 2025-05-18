from dataclasses import dataclass

from pyfecons.costing.categories.cas900000 import CAS90
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS90Section(ReportSection):
    def __init__(self, cas90: CAS90):
        super().__init__()
        self.template_file = "CAS900000.tex"
        self.replacements = {"C900000": str(round(cas90.C900000))}
