from dataclasses import dataclass

from pyfecons.costing.accounting.npv import NPV
from pyfecons.inputs.npv_Input import NpvInput
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class NpvSection(ReportSection):
    def __init__(self, npv: NPV, npv_input: NpvInput):
        super().__init__()
        self.template_file = "NPV.tex"
        self.replacements = {
            "NPVval": str(round(npv.npv, 2)),
            "DiscountRate": str(
                round(npv_input.discount_rate * 100, 2)
            ),  # Multiplied by 100 for percentage
        }
