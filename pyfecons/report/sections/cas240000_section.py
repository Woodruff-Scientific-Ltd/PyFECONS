from dataclasses import dataclass

from pyfecons.costing.categories.cas240000 import CAS24
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS24Section(ReportSection):
    def __init__(self, cas24: CAS24):
        super().__init__()
        self.template_file = "CAS240000.tex"
        self.replacements = {"C240000": str(round(cas24.C240000, 1))}
