from dataclasses import dataclass

from pyfecons.costing.categories.cas220200 import CAS2202
from pyfecons.inputs.blanket import Blanket
from pyfecons.report.section import ReportSection


@dataclass
class CAS2202Section(ReportSection):
    def __init__(self, cas2202: CAS2202, blanket: Blanket):
        super().__init__()
        self.template_file = "CAS220200_DT.tex"
        self.replacements = {
            "C220200": str(round(cas2202.C220200)),
            "C220201": str(round(cas2202.C220201)),
            "C220202": str(round(cas2202.C220202)),
            "C220203": str(round(cas2202.C220203)),  # TODO not in template
            "primaryC": blanket.primary_coolant.display_name,
            "secondaryC": blanket.secondary_coolant.display_name,
        }
