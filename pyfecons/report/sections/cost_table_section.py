from dataclasses import dataclass

from pyfecons.costing_data import CostingData
from pyfecons.enums import ReactorType
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
        reactor_type: ReactorType,
    ):
        super().__init__()
        self.template_file = "CASstructure.tex"
        if reactor_type == ReactorType.MFE:
            self.replacements = get_mfe_replacements(costing_data)
        elif reactor_type == ReactorType.IFE:
            self.replacements = get_ife_replacements(costing_data)
        else:
            raise ValueError(f"Unsupported reactor type: {reactor_type}")
