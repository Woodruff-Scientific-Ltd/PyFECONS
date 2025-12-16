from dataclasses import dataclass

from pyfecons.costing.categories.cas800000 import CAS80
from pyfecons.enums import FusionMachineType
from pyfecons.inputs.blanket import Blanket
from pyfecons.report.section import ReportSection


@dataclass
class CAS80Section(ReportSection):
    def __init__(
        self,
        cas80: CAS80,
        fusion_machine_type: FusionMachineType,
        blanket: Blanket,
    ):
        super().__init__()
        if fusion_machine_type == FusionMachineType.MFE:
            self._init_mfe(cas80, blanket)
        elif fusion_machine_type == FusionMachineType.IFE:
            self._init_ife(cas80)
        else:
            raise ValueError(f"Unsupported reactor type: {fusion_machine_type}")

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
