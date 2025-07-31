from dataclasses import dataclass, field

from pyfecons.serializable import SerializableToJSON


@dataclass
class ReportSection(SerializableToJSON):
    # template substitutions variable_name -> value
    replacements: dict[str, str] = field(default_factory=dict)
    # template file name in templates/ directory
    template_file: str = None
    # latex path -> image bytes
    figures: dict[str, bytes] = field(default_factory=dict)
    # template file path for LaTeX compilation directory (defaults to Modified/{template_file})
    _tex_path: str = None

    @property
    def tex_path(self) -> str:
        if self._tex_path is None:
            return "Modified/" + self.template_file
        return self._tex_path

    @tex_path.setter
    def tex_path(self, value):
        self._tex_path = value
