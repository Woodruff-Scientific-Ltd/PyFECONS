from typing import Optional

from pyfecons.costing_data import CostingData
from pyfecons.helpers import get_local_included_files_map
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.report import (
    ReportContent,
    ReportOverrides,
    combine_figures,
    get_report_sections,
)
from pyfecons.templates import hydrate_templates, load_document_template

TEMPLATES_PATH = "pyfecons.costing.mfe.templates"
INCLUDED_FILES_PATH = "pyfecons.costing.mfe.included_files"
DOCUMENT_TEMPLATE = "Costing_ARPA-E_MFE_Modified.tex"

# list representing latex_path in included_files directory
LOCAL_INCLUDED_FILES = [
    "additions.bib",
    "glossary.tex",
    "IEEEtran.bst",
    "ST-SC.bib",
    "Figures/cooling_efficiency.pdf",
    "Figures/MFE.png",
    "Originals/CAS220100_MFE.tex",
    "Originals/method.tex",
    "Originals/powerBalanceMFEDT.tex",
    "StandardFigures/TIsketch.eps",
    "StandardFigures/WSLTD_logo.png",
    "StandardFigures/costcategories.png",
    "StandardFigures/power.eps",
    "StandardFigures/signature.jpg",
    "StandardFigures/siteplan2023.eps",
    "StandardFigures/statista.png",
    "StandardFigures/steamPbLi-eps-converted-to.pdf",
    "StandardFigures/yuhu_cs.pdf",
]


def CreateReportContent(
    inputs: AllInputs,
    costing_data: CostingData,
    overrides: Optional[ReportOverrides] = None,
) -> ReportContent:
    document_template = load_document_template(
        TEMPLATES_PATH, DOCUMENT_TEMPLATE, overrides
    )
    report_sections = get_report_sections(inputs, costing_data)
    hydrated_templates = hydrate_templates(TEMPLATES_PATH, report_sections, overrides)
    figures = combine_figures(report_sections)
    included_files = get_local_included_files_map(
        INCLUDED_FILES_PATH, LOCAL_INCLUDED_FILES, overrides
    )
    return ReportContent(
        document_template, hydrated_templates, report_sections, included_files, figures
    )
