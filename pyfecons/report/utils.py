from typing import List, Dict

from pyfecons.costing_data import CostingData
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.report.section import ReportSection
from pyfecons.report.sections.cas100000_section import CAS10Section
from pyfecons.report.sections.cas200000_section import CAS20Section
from pyfecons.report.sections.cas220000_section import CAS22Section
from pyfecons.report.sections.cas220104_section import CAS220104Section
from pyfecons.report.sections.cas220105_section import CAS220105Section
from pyfecons.report.sections.cas220106_section import CAS220106Section
from pyfecons.report.sections.cas220107_section import CAS220107Section
from pyfecons.report.sections.cas220108_section import CAS220108Section
from pyfecons.report.sections.cas220109_section import CAS220109Section
from pyfecons.report.sections.cas220111_section import CAS220111Section
from pyfecons.report.sections.cas220119_section import CAS220119Section
from pyfecons.report.sections.cas220200_section import CAS2202Section
from pyfecons.report.sections.cas220300_section import CAS2203Section
from pyfecons.report.sections.cas220400_section import CAS2204Section
from pyfecons.report.sections.cas220500_section import CAS2205Section
from pyfecons.report.sections.cas220600_section import CAS2206Section
from pyfecons.report.sections.cas220700_section import CAS2207Section
from pyfecons.report.sections.cas230000_section import CAS23Section
from pyfecons.report.sections.cas250000_section import CAS25Section
from pyfecons.report.sections.cas260000_section import CAS26Section
from pyfecons.report.sections.cas270000_section import CAS27Section
from pyfecons.report.sections.cas280000_section import CAS28Section
from pyfecons.report.sections.cas290000_section import CAS29Section
from pyfecons.report.sections.cas300000_section import CAS30Section
from pyfecons.report.sections.power_table_section import PowerTableSection
from pyfecons.report.sections.cas210000_section import CAS21Section
from pyfecons.report.sections.cas220101_section import CAS220101Section
from pyfecons.report.sections.cas220102_section import CAS220102Section
from pyfecons.report.sections.cas220103_section import CAS220103Section
from pyfecons.report.sections.cas240000_section import CAS24Section


def get_report_sections(
    inputs: AllInputs, costing_data: CostingData
) -> List[ReportSection]:
    """Get all report sections with their templates and replacements."""
    reactor_type = inputs.basic.reactor_type
    return [
        PowerTableSection(costing_data.power_table, inputs.basic, inputs.power_input),
        CAS10Section(costing_data.cas10, inputs.basic),
        CAS21Section(costing_data.cas21),
        CAS220101Section(
            costing_data.cas220101, inputs.basic, inputs.radial_build, inputs.blanket
        ),
        CAS220102Section(costing_data.cas220102, reactor_type),
        CAS220103Section(
            costing_data.cas220103,
            reactor_type,
            inputs.power_input,
            inputs.lasers,
            inputs.coils,
        ),
        CAS220104Section(
            costing_data.cas220104,
            reactor_type,
            inputs.supplementary_heating,
            costing_data.cas220103,
        ),
        CAS220105Section(
            costing_data.cas220105, inputs.basic, inputs.primary_structure
        ),
        CAS220106Section(costing_data.cas220106, reactor_type, inputs.vacuum_system),
        CAS220107Section(costing_data.cas220107, inputs.basic, inputs.power_supplies),
        CAS220108Section(costing_data.cas220108, reactor_type),
        CAS220109Section(costing_data.cas220109),
        CAS220111Section(costing_data.cas220111, inputs.basic, inputs.installation),
        CAS220119Section(costing_data.cas220119),
        CAS2202Section(costing_data.cas2202, inputs.blanket),
        CAS2203Section(costing_data.cas2203),
        CAS2204Section(costing_data.cas2204),
        CAS2205Section(costing_data.cas2205, inputs.fuel_handling),
        CAS2206Section(costing_data.cas2206),
        CAS2207Section(costing_data.cas2207),
        CAS22Section(costing_data.cas22),
        CAS23Section(costing_data.cas23),
        CAS24Section(costing_data.cas24),
        CAS25Section(costing_data.cas25),
        CAS26Section(costing_data.cas26),
        CAS27Section(costing_data.cas27),
        CAS28Section(costing_data.cas28),
        CAS29Section(costing_data.cas29),
        CAS20Section(costing_data.cas20),
        CAS30Section(costing_data.cas30, inputs.basic),
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
