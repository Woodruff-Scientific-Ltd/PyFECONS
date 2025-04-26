from dataclasses import dataclass

from pyfecons.costing.categories.cas220119 import CAS220119
from pyfecons.report.section import ReportSection


@dataclass
class CAS220119Section(ReportSection):
    """Report section for CAS220105 primary structure."""

    def __init__(self, cas220119: CAS220119):
        super().__init__()
        self.template_file = "CAS220119.tex"
        self.replacements = {"C220119": str(round(cas220119.C220119))}
