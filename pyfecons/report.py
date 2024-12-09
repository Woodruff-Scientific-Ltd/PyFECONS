from dataclasses import dataclass, field

from pyfecons.data import Data, TemplateProvider


@dataclass
class CostingData:
    data: Data = None
    template_providers: list[TemplateProvider] = None

    def __post_init__(self):
        if self.template_providers is None:
            self.template_providers = []


@dataclass
class HydratedTemplate:
    template_provider: TemplateProvider = None
    contents: str = None


@dataclass
class ReportContent:
    # Top level document file as base of tex compilation
    document_template: HydratedTemplate = None
    # Hydrated templates to be included in tex compilation
    hydrated_templates: list[HydratedTemplate] = field(default_factory=list)
    # tex file path -> absolute path of files to include in tex compilation
    included_files: dict[str, str] = field(default_factory=dict)
    # latex path -> image bytes
    figures: dict[str, bytes] = field(default_factory=dict)


@dataclass
class FinalReport:
    report_tex: str
    report_pdf: bytes


@dataclass
class ReportOverrides:
    # tex_file_path -> absolute path of included_file to be overridden
    included_files: dict[str, str] = field(default_factory=dict)
    # template_filename -> contents of templates to be overridden in hydration
    templates: dict[str, str] = field(default_factory=dict)
