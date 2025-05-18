from dataclasses import dataclass

from pyfecons.costing.categories.cas280000 import CAS28
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS28Section(ReportSection):
    def __init__(self, cas28: CAS28):
        super().__init__()
        self.template_file = "CAS280000.tex"
        self.replacements = {"C280000": str(cas28.C280000)}
