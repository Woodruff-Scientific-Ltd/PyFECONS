from dataclasses import dataclass

from pyfecons.costing.categories.cas220107 import CAS220107
from pyfecons.enums import FusionMachineType
from pyfecons.figures.cap_derate import CapDerateFigure
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.power_supplies import PowerSupplies
from pyfecons.report.section import ReportSection


@dataclass
class CAS220107Section(ReportSection):
    def __init__(
        self,
        cas220107: CAS220107,
        basic: Basic,
        power_supplies: PowerSupplies,
    ):
        super().__init__()
        if basic.fusion_machine_type == FusionMachineType.MFE:
            self._init_mfe(cas220107, basic)
        elif basic.fusion_machine_type == FusionMachineType.IFE:
            self._init_ife(cas220107, basic, power_supplies)
        else:
            raise ValueError(f"Unsupported reactor type: {basic.fusion_machine_type}")

    def _init_mfe(self, cas220107: CAS220107, basic: Basic):
        self.template_file = "CAS220107_MFE.tex"
        self.replacements = {
            "C22010700": str(round(cas220107.C220107)),
            "C22010701": str(round(cas220107.C22010701)),
            "C22010702": str(round(cas220107.C22010702)),
            "PNRL": str(round(basic.p_nrl)),
        }

    def _init_ife(
        self, cas220107: CAS220107, basic: Basic, power_supplies: PowerSupplies
    ):
        self.template_file = "CAS220107_IFE.tex"
        self.replacements = {
            "C22010700": str(round(cas220107.C220107)),
            "C22010701": str(round(cas220107.C22010701)),  # TODO not in template
            "C22010702": str(round(cas220107.C22010702)),  # TODO not in template
            "PNRL": str(round(basic.p_nrl)),
        }
        # TODO figure is not rendering anything and it's not used in the template
        self.figures["Figures/cap_derate.pdf"] = CapDerateFigure.create(
            power_supplies, basic.implosion_frequency
        )
