from dataclasses import dataclass
from typing import Dict, Any

from pyfecons.report.section import ReportSection
from pyfecons.costing.categories.cas210000 import CAS21


@dataclass
class CAS21Section(ReportSection):
    def __init__(self, cas21: CAS21):
        super().__init__()
        self.template_file = "CAS210000.tex"
        self.replacements = {
            "C210000": str(round(cas21.C210000, 1)),
            "C210100": str(round(cas21.C210100, 1)),
            "C210200": str(round(cas21.C210200, 1)),
            "C210300": str(round(cas21.C210300, 1)),
            "C210400": str(round(cas21.C210400, 1)),
            "C210500": str(round(cas21.C210500, 1)),
            "C210600": str(round(cas21.C210600, 1)),
            "C210700": str(round(cas21.C210700, 1)),
            "C210800": str(round(cas21.C210800, 1)),
            "C210900": str(round(cas21.C210900, 1)),
            "C211000": str(round(cas21.C211000, 1)),
            "C211100": str(round(cas21.C211100, 1)),
            "C211200": str(round(cas21.C211200, 1)),
            "C211300": str(round(cas21.C211300, 1)),
            "C211400": str(round(cas21.C211400, 1)),
            "C211500": str(round(cas21.C211500, 1)),
            "C211600": str(round(cas21.C211600, 1)),
            "C211700": str(round(cas21.C211700, 1)),
            "C211900": str(round(cas21.C211900, 1)),  # TODO - not in the template file
        }
