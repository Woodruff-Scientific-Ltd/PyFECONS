from dataclasses import dataclass

from pyfecons.costing.categories.cas500000 import CAS50
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS50Section(ReportSection):
    def __init__(self, cas50: CAS50):
        super().__init__()
        self.template_file = "CAS500000.tex"
        self.replacements = {
            "C500000": str(round(cas50.C500000)),  # TODO - not in template
            "C510000": str(round(cas50.C510000)),
            "C520000": str(round(cas50.C520000)),
            "C530000": str(round(cas50.C530000)),
            "C540000": str(round(cas50.C540000)),
            "C550000": str(round(cas50.C550000)),
            "C580000": str(round(cas50.C580000)),
            "C590000": str(round(cas50.C590000)),
        }
