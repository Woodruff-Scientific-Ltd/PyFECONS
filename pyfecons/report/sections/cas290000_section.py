from dataclasses import dataclass

from pyfecons.costing.categories.cas290000 import CAS29
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS29Section(ReportSection):
    def __init__(self, cas29: CAS29):
        super().__init__()
        self.template_file = "CAS290000.tex"
        self.replacements = {"C290000": str(round(cas29.C290000))}
