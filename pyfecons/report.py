from dataclasses import dataclass


@dataclass
class ReportContent:
    # filename -> contents
    hydrated_templates: dict[str, str] = None
    # tex file path -> local file path of files to include in tex compilation
    included_files: dict[str, str] = None


@dataclass
class FinalReport:
    report_tex: str
    report_pdf: bytes
