from dataclasses import dataclass


@dataclass
class ReportContent:
    # TODO convert hydrated templates to an ordered list
    # filename -> contents
    hydrated_templates: dict[str, str] = None
    # filename -> contents
    included_files: dict[str, str] = None
    latex_packages: list[str] = None


@dataclass
class FinalReport:
    report_tex: str
    report_pdf: bytes
