from dataclasses import dataclass

from pyfecons.costing.categories.cas220400 import CAS2204
from pyfecons.report.section import ReportSection


@dataclass
class CAS2204Section(ReportSection):
    def __init__(self, cas2204: CAS2204):
        super().__init__()
        self.template_file = "CAS220400.tex"
        self.replacements = {"C220400": str(round(cas2204.C220400, 1))}
