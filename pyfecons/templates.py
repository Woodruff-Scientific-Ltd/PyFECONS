from importlib import resources
from pyfecons.report import TemplateProvider, HydratedTemplate


def read_template(templates_path: str, template_file: str) -> str:
    with resources.path(templates_path, template_file) as template_path:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()


def replace_values(template_content: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        template_content = template_content.replace(key, str(value))
    return template_content


def hydrate_templates(templates_path: str, template_providers: list[TemplateProvider]) -> list[HydratedTemplate]:
    hydrated_templates = []
    for provider in template_providers:
        template_content = read_template(templates_path, provider.template_file)
        contents = replace_values(template_content, provider.replacements)
        hydrated_templates.append(HydratedTemplate(provider, contents))
    return hydrated_templates


def combine_figures(template_providers: list[TemplateProvider]) -> dict[str, bytes]:
    all_figures = {}
    for provider in template_providers:
        all_figures.update(provider.figures)
    return all_figures
