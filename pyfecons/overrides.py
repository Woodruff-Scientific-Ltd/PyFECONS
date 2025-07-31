from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ReportOverrides:
    """Overrides for report generation."""

    included_files: Dict[str, str] = field(default_factory=dict)
    template_overrides: Optional[Dict[str, Any]] = None
    templates: Dict[str, str] = field(default_factory=dict)
