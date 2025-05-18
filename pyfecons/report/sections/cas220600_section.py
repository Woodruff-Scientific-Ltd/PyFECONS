from dataclasses import dataclass

from pyfecons.costing.categories.cas220600 import CAS2206
from pyfecons.report.section import ReportSection


@dataclass
class CAS2206Section(ReportSection):
    def __init__(self, cas2206: CAS2206):
        super().__init__()
        self.template_file = "CAS220600.tex"
        self.replacements = {"C220600": str(round(cas2206.C220600))}
