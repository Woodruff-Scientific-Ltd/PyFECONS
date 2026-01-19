from dataclasses import dataclass

from pyfecons.costing.categories.cas220120 import CAS220120
from pyfecons.report.section import ReportSection


@dataclass
class CAS220120Section(ReportSection):
    def __init__(self, cas220120: CAS220120):
        super().__init__()
        self.template_file = "CAS220120.tex"
        self.replacements = {"C220120": str(round(cas220120.C220120, 1))}
