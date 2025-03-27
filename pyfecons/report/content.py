from dataclasses import dataclass, field
from pyfecons.report.hydrated_template import HydratedTemplate


@dataclass
class ReportContent:
    # Top level document file as base of tex compilation
    document_template: HydratedTemplate
    # Hydrated templates to be included in tex compilation
    hydrated_templates: list[HydratedTemplate]
    # tex file path -> absolute path of files to include in tex compilation
    included_files: dict[str, str] = field(default_factory=dict)
    # latex path -> image bytes
    figures: dict[str, bytes] = field(default_factory=dict) 