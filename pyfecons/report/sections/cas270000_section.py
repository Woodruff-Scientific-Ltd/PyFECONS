from dataclasses import dataclass

from pyfecons.costing.categories.cas270000 import CAS27
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS27Section(ReportSection):
    def __init__(self, cas27: CAS27):
        super().__init__()
        self.template_file = "CAS270000.tex"
        self.replacements = {"C270000": round(cas27.C270000)}
