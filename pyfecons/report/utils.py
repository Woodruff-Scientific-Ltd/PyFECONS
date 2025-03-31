from typing import List, Dict

from pyfecons.costing_data import CostingData
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.report.section import ReportSection
from pyfecons.report.sections.cas10_section import CAS10Section
from pyfecons.report.sections.power_table_section import PowerTableSection
from pyfecons.report.sections.cas21_section import CAS21Section
from pyfecons.report.sections.cas220101_section import CAS220101Section


def get_report_sections(
    inputs: AllInputs, costing_data: CostingData
) -> List[ReportSection]:
    """Get all report sections with their templates and replacements."""
    return [
        PowerTableSection(costing_data.power_table, inputs.basic, inputs.power_input),
        CAS10Section(costing_data.cas10, inputs.basic),
        CAS21Section(costing_data.cas21),
        CAS220101Section(
            costing_data.cas220101,
            inputs.basic,
            inputs.radial_build,
            inputs.blanket
        ),
        costing_data.cas220102,
        costing_data.cas220103,
        costing_data.cas220104,
        costing_data.cas220105,
        costing_data.cas220106,
        costing_data.cas220107,
        costing_data.cas220108,
        costing_data.cas220109,
        costing_data.cas220111,
        costing_data.cas220119,
        costing_data.cas2202,
        costing_data.cas2203,
        costing_data.cas2204,
        costing_data.cas2205,
        costing_data.cas2206,
        costing_data.cas2207,
        costing_data.cas22,
        costing_data.cas23,
        costing_data.cas24,
        costing_data.cas25,
        costing_data.cas26,
        costing_data.cas27,
        costing_data.cas28,
        costing_data.cas29,
        costing_data.cas20,
        costing_data.cas30,
        costing_data.cas40,
        costing_data.cas50,
        costing_data.cas60,
        costing_data.cas70,
        costing_data.cas80,
        costing_data.cas90,
        costing_data.lcoe,
        costing_data.cost_table,
        costing_data.npv,
    ]


def combine_figures(report_sections: List[ReportSection]) -> Dict[str, bytes]:
    """Combine figures from all report sections into a single dictionary."""
    figures = {}
    for section in report_sections:
        figures.update(section.figures)
    return figures
