from dataclasses import dataclass, field
from pyfecons.report.hydrated_template import HydratedTemplate
from pyfecons.report.section import ReportSection


@dataclass
class ReportContent:
    # Top level document file as base of tex compilation
    document_template: HydratedTemplate
    # Hydrated templates to be included in tex compilation
    hydrated_templates: list[HydratedTemplate]
    # Original report sections used to generate content
    report_sections: list[ReportSection]
    # tex file path -> absolute path of files to include in tex compilation
    included_files: dict[str, str] = field(default_factory=dict)
    # latex path -> image bytes
    figures: dict[str, bytes] = field(default_factory=dict) 