from dataclasses import dataclass
from pyfecons.report.section import ReportSection


@dataclass
class HydratedTemplate:
    template_provider: ReportSection
    contents: str
