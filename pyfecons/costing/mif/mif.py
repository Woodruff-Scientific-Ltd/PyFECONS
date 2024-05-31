from pyfecons.data import Data, TemplateProvider
from pyfecons.enums import ReactorType
from pyfecons.helpers import get_local_included_files_map
from pyfecons.inputs import Inputs
from pyfecons.report import CostingData, ReportContent, HydratedTemplate
from pyfecons.templates import hydrate_templates, combine_figures, read_template

TEMPLATES_PATH = 'pyfecons.costing.mif.templates'
INCLUDED_FILES_PATH = 'pyfecons.costing.mif.included_files'
DOCUMENT_TEMPLATE = 'Costing_ARPA-E_MIF_Modified.tex'

# list representing latex_path in included_files directory
INCLUDED_FILES = [
    'additions.bib',
    'glossary.tex',
    'IEEEtran.bst',
    'ST-SC.bib',
    'Figures/FrontMatter.eps',
    'Originals/CAS220100_MIF.tex',
    'Originals/method.tex',
    'Originals/powerBalanceMIFDT.tex',
    'StandardFigures/costcategories.png',
    'StandardFigures/signature.jpg',
    'StandardFigures/power.eps',
    'StandardFigures/WSLTD_logo.png',
]


def GenerateCostingData(inputs: Inputs) -> CostingData:
    data = Data(reactor_type=ReactorType.MIF)
    template_providers = []
    return CostingData(data, template_providers)


def CreateReportContent(costing_data: CostingData) -> ReportContent:
    document_template = load_document_template()
    hydrated_templates = hydrate_templates(TEMPLATES_PATH, costing_data.template_providers)
    figures = combine_figures(costing_data.template_providers)
    included_files = get_local_included_files_map(INCLUDED_FILES_PATH, INCLUDED_FILES)
    return ReportContent(document_template, hydrated_templates, included_files, figures)


def load_document_template() -> HydratedTemplate:
    return HydratedTemplate(
        TemplateProvider(template_file=DOCUMENT_TEMPLATE),
        read_template(TEMPLATES_PATH, DOCUMENT_TEMPLATE)
    )