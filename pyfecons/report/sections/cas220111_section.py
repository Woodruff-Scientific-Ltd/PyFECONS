from dataclasses import dataclass

from pyfecons.costing.categories.cas220111 import CAS220111
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.installation import Installation
from pyfecons.report.section import ReportSection


@dataclass
class CAS220111Section(ReportSection):
    def __init__(self, cas220111: CAS220111, basic: Basic, installation: Installation):
        super().__init__()
        self.template_file = "CAS220111.tex"
        self.replacements = {
            "C220111": str(cas220111.C220111),
            "constructionTime": str(round(basic.construction_time)),
            "billingRate": str(round(installation.labor_rate)),
        }
