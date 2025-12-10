from importlib import resources


def load_document_template(template_path: str) -> str:
    """Load a document template from the templates directory."""
    return resources.files("pyfecons.templates").joinpath(template_path).read_text()
