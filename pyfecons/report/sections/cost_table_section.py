from dataclasses import dataclass

from pyfecons.costing_data import CostingData
from pyfecons.enums import FusionMachineType
from pyfecons.report.cost_table.cost_table_ife import (
    get_replacements as get_ife_replacements,
)
from pyfecons.report.cost_table.cost_table_mfe import (
    get_replacements as get_mfe_replacements,
)
from pyfecons.report.section import ReportSection


@dataclass
class CostTableSection(ReportSection):
    def __init__(
        self,
        costing_data: CostingData,
        fusion_machine_type: FusionMachineType,
    ):
        super().__init__()
        self.template_file = "CASstructure.tex"
        if fusion_machine_type == FusionMachineType.MFE:
            self.replacements = get_mfe_replacements(costing_data)
        elif fusion_machine_type == FusionMachineType.IFE:
            self.replacements = get_ife_replacements(costing_data)
        else:
            raise ValueError(f"Unsupported reactor type: {fusion_machine_type}")
