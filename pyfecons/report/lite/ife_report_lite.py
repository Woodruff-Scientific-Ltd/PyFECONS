from typing import Optional

from pyfecons.costing_data import CostingData
from pyfecons.helpers import get_local_included_files_map
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.report import ReportContent, ReportOverrides, combine_figures
from pyfecons.report.lite.utils import get_report_sections_lite
from pyfecons.templates import hydrate_templates, load_document_template

TEMPLATES_PATH = "pyfecons.costing.ife.templates.lite"
INCLUDED_FILES_PATH = "pyfecons.costing.ife.included_files.lite"
DOCUMENT_TEMPLATE = "Costing_ARPA-E_IFE_Lite.tex"

# list representing latex_path in included_files directory
# Note: StandardFigures, Figures, and bibliography files need to be copied from parent included_files
LOCAL_INCLUDED_FILES = [
    "cover_page.tex",
    "methodology_summary.tex",
]


def CreateReportContentLite(
    inputs: AllInputs,
    costing_data: CostingData,
    overrides: Optional[ReportOverrides] = None,
) -> ReportContent:
    document_template = load_document_template(
        TEMPLATES_PATH, DOCUMENT_TEMPLATE, overrides
    )
    report_sections = get_report_sections_lite(inputs, costing_data)

    # Modify template_file paths to use lite templates
    for section in report_sections:
        if section.template_file == "powerTableIFEDT.tex":
            section.template_file = "powerTableIFEDT.tex"
        elif section.template_file == "CASstructure.tex":
            section.template_file = "CASstructure.tex"
        elif section.template_file == "LCOE.tex":
            section.template_file = "LCOE.tex"

    # Use the lite templates path
    hydrated_templates = hydrate_templates(TEMPLATES_PATH, report_sections, overrides)
    figures = combine_figures(report_sections)
    included_files = get_local_included_files_map(
        INCLUDED_FILES_PATH, LOCAL_INCLUDED_FILES, overrides
    )

    # Add StandardFigures, Figures, and bibliography files from parent included_files directory
    from pyfecons.helpers import get_included_file_path

    parent_included_files_path = "pyfecons.costing.ife.included_files"
    included_files["StandardFigures/catf-logo.png"] = get_included_file_path(
        parent_included_files_path, "StandardFigures/catf-logo.png", overrides
    )
    included_files["Figures/FastIgnition.png"] = get_included_file_path(
        parent_included_files_path, "Figures/FastIgnition.png", overrides
    )
    included_files["ST-SC.bib"] = get_included_file_path(
        parent_included_files_path, "ST-SC.bib", overrides
    )
    included_files["additions.bib"] = get_included_file_path(
        parent_included_files_path, "additions.bib", overrides
    )
    included_files["IEEEtran.bst"] = get_included_file_path(
        parent_included_files_path, "IEEEtran.bst", overrides
    )

    return ReportContent(
        document_template, hydrated_templates, report_sections, included_files, figures
    )
