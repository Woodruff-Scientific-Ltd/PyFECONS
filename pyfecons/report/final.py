from dataclasses import dataclass


@dataclass
class FinalReport:
    report_tex: str
    report_pdf: bytes
