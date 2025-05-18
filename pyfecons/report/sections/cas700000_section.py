from dataclasses import dataclass

from pyfecons.costing.categories.cas700000 import CAS70
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS70Section(ReportSection):
    def __init__(self, cas70: CAS70):
        super().__init__()
        self.template_file = "CAS700000.tex"
        self.replacements = {"C700000": str(round(cas70.C700000))}
