from dataclasses import dataclass

from pyfecons import Data, TemplateProvider


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
    hydrated_templates: list[HydratedTemplate] = None
    # tex file path -> local file path of files to include in tex compilation
    included_files: dict[str, str] = None


@dataclass
class FinalReport:
    report_tex: str
    report_pdf: bytes
