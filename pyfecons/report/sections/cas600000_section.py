from dataclasses import dataclass

from pyfecons.costing.categories.cas600000 import CAS60
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS60Section(ReportSection):
    def __init__(self, cas60: CAS60):
        super().__init__()
        self.template_file = "CAS600000.tex"
        self.replacements = {
            "C600000": str(round(cas60.C600000)),  # TODO - not in template
            "C610000": str(round(cas60.C610000)),
            "C630000LSA": str(round(cas60.C630000LSA)),
            "C630000XXX": str(round(cas60.C630000)),
        }
