from dataclasses import dataclass, field


@dataclass
class TemplateProvider:
    # template substitutions variable_name -> value
    replacements: dict[str, str] = field(default_factory=dict)
    # template file name in templates/ directory
    template_file: str = None
    # latex path -> image bytes
    figures: dict[str, bytes] = field(default_factory=dict)
    # template file path for LaTeX compilation directory (defaults to Modified/{template_file})
    _tex_path: str = None

    # TODO - tex_path is not serializing right now and I can't figure out how to get it to work
    # https://chatgpt.com/share/fab6081c-35fb-41e7-bf9a-a4e2e188865f
    @property
    def tex_path(self) -> str:
        if self._tex_path is None:
            return "Modified/" + self.template_file
        return self._tex_path

    @tex_path.setter
    def tex_path(self, value):
        self._tex_path = value


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
