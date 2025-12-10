from dataclasses import dataclass

from pyfecons.costing.categories.cas220700 import CAS2207
from pyfecons.report.section import ReportSection


@dataclass
class CAS2207Section(ReportSection):
    def __init__(self, cas2207: CAS2207):
        super().__init__()
        self.template_file = "CAS220700.tex"
        self.replacements = {"C220700": str(round(cas2207.C220700))}
