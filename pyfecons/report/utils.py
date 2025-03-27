from typing import List, Dict

from pyfecons.costing_data import CostingData
from pyfecons.report.section import ReportSection


def get_report_sections(costing_data: CostingData) -> List[ReportSection]:
    """Get all report sections from costing data."""
    return [
        section for section in costing_data.__dict__.values()
        if isinstance(section, ReportSection)
    ]


def combine_figures(report_sections: List[ReportSection]) -> Dict[str, bytes]:
    """Combine figures from all report sections into a single dictionary."""
    figures = {}
    for section in report_sections:
        figures.update(section.figures)
    return figures 