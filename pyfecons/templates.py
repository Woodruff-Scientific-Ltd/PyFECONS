from importlib import resources
from typing import Optional

from pyfecons.report import HydratedTemplate, ReportOverrides, ReportSection


def read_template(templates_path: str, template_file: str) -> str:
    with resources.path(templates_path, template_file) as template_path:
        with open(template_path, "r", encoding="utf-8") as file:
            return file.read()


def replace_values(template_content: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        template_content = template_content.replace(key, str(value))
    return template_content


def hydrate_templates(
    templates_path: str,
    template_providers: list[ReportSection],
    overrides: Optional[ReportOverrides] = None,
) -> list[HydratedTemplate]:
    hydrated_templates = []
    for provider in template_providers:
        template_content = get_template_contents(
            templates_path, provider.template_file, overrides
        )
        contents = replace_values(template_content, provider.replacements)
        hydrated_templates.append(HydratedTemplate(provider, contents))
    return hydrated_templates


def combine_figures(template_providers: list[ReportSection]) -> dict[str, bytes]:
    all_figures = {}
    for provider in template_providers:
        all_figures.update(provider.figures)
    return all_figures


def load_document_template(
    templates_path: str,
    document_template: str,
    overrides: Optional[ReportOverrides] = None,
) -> HydratedTemplate:
    return HydratedTemplate(
        ReportSection(template_file=document_template),
        get_template_contents(templates_path, document_template, overrides),
    )


def get_template_contents(
    templates_path: str, template_file: str, overrides: Optional[ReportOverrides] = None
) -> str:
    if overrides is not None and template_file in overrides.templates.keys():
        return overrides.templates[template_file]
    else:
        return read_template(templates_path, template_file)
