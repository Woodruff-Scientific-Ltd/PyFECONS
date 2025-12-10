from dataclasses import dataclass

from pyfecons.costing.categories.cas220300 import CAS2203
from pyfecons.report.section import ReportSection


@dataclass
class CAS2203Section(ReportSection):
    def __init__(self, cas2203: CAS2203):
        super().__init__()
        self.template_file = "CAS220300.tex"
        self.replacements = {"C220300": str(round(cas2203.C220300, 1))}
