from dataclasses import dataclass

from pyfecons.costing.categories.cas800000 import CAS80
from pyfecons.enums import ReactorType
from pyfecons.inputs.blanket import Blanket
from pyfecons.report.section import ReportSection


@dataclass
class CAS80Section(ReportSection):
    def __init__(
        self,
        cas80: CAS80,
        reactor_type: ReactorType,
        blanket: Blanket,
    ):
        super().__init__()
        if reactor_type == ReactorType.MFE:
            self._init_mfe(cas80, blanket)
        elif reactor_type == ReactorType.IFE:
            self._init_ife(cas80)
        else:
            raise ValueError(f"Unsupported reactor type: {reactor_type}")

    def _init_mfe(self, cas80: CAS80, blanket: Blanket):
        self.template_file = "CAS800000_DT.tex"
        self.replacements = {
            "C800000": str(round(cas80.C800000, 2)),
            "primaryC": blanket.primary_coolant.display_name,
            "secondaryC": blanket.secondary_coolant.display_name,
        }

    def _init_ife(self, cas80: CAS80):
        self.template_file = "CAS800000_DT.tex"
        self.replacements = {"C800000": str(round(cas80.C800000))}
