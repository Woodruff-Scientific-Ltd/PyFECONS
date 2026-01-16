from typing import List

from pyfecons.costing_data import CostingData
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.report.section import ReportSection
from pyfecons.report.sections.cost_table_section import CostTableSection
from pyfecons.report.sections.lcoe_section import LcoeSection
from pyfecons.report.sections.power_table_section import PowerTableSection


def get_report_sections_lite(
    inputs: AllInputs, costing_data: CostingData
) -> List[ReportSection]:
    """Get lite report sections: only Power Table, Cost Table, and LCOE."""
    return [
        PowerTableSection(costing_data.power_table, inputs.basic, inputs.power_input),
        CostTableSection(costing_data, inputs.basic.fusion_machine_type),
        LcoeSection(
            costing_data.lcoe,
            inputs.basic,
            costing_data.power_table,
            costing_data.cas70,
            costing_data.cas80,
            costing_data.cas90,
        ),
    ]
