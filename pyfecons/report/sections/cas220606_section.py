from dataclasses import dataclass

from pyfecons.costing.categories.cas220606 import CAS220606
from pyfecons.report.section import ReportSection


@dataclass
class CAS220606Section(ReportSection):
    def __init__(self, cas220606: CAS220606):
        super().__init__()
        self.template_file = "CAS220606.tex"
        self.replacements = {"C220606": str(round(cas220606.C220606, 1))}
