from importlib import resources

from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.report import CostingData, ReportContent, HydratedTemplate
from pyfecons.templates import read_template, hydrate_templates
from pyfecons.costing.ife.PowerBalance import GenerateData as PowerBalanceData
from pyfecons.costing.ife.CAS10 import GenerateData as CAS10Data
from pyfecons.costing.ife.CAS21 import GenerateData as CAS21Data

TEMPLATES_PATH = 'pyfecons.costing.ife.templates'
INCLUDED_FILES_PATH = 'pyfecons.costing.ife.included_files'
DOCUMENT_TEMPLATE='Costing_ARPA-E_IFE_Modified.tex'

# map of latex_path -> included_file_name
LOCAL_INCLUDED_FILES = {
    'StandardFigures/WSLTD_logo.png': 'WSLTD_logo.png',
    'Figures/FastIgnition.png': 'FastIgnition.png',
    'StandardFigures/signature.jpg': 'signature.jpg',
    'Originals/method.tex': 'method.tex',
    'Originals/powerBalanceIFEDT.tex': 'powerBalanceIFEDT.tex',
    'Originals/CAS220100_IFE.tex': 'CAS220100_IFE.tex',
    'glossary.tex': 'glossary.tex',
    'IEEEtran.bst': 'IEEEtran.bst',
    'ST-SC.bib': 'ST-SC.bib',
    'additions.bib': 'additions.bib',
    'StandardFigures/costcategories.png': 'costcategories.png',
    'StandardFigures/power.eps': 'power.eps',
    'StandardFigures/siteplan2023.eps': 'siteplan2023.eps',
}


def GenerateCostingData(inputs: Inputs) -> CostingData:
    data = Data()
    template_providers = (
        PowerBalanceData(inputs, data)
        + CAS10Data(inputs, data)
        + CAS21Data(inputs, data)
    )
    return CostingData(data, template_providers)


def CreateReportContent(costing_data: CostingData) -> ReportContent:
    document_template = load_document_template()
    hydrated_templates = hydrate_templates(TEMPLATES_PATH, costing_data.template_providers)
    included_files = get_included_files_map()
    return ReportContent(document_template, hydrated_templates, included_files)


def get_included_files_map() -> dict[str, str]:
    file_map = {}
    for tex_path, template_file in LOCAL_INCLUDED_FILES.items():
        with resources.path(INCLUDED_FILES_PATH, template_file) as res_path:
            file_map[tex_path] = str(res_path)
    return file_map


def load_document_template() -> HydratedTemplate:
    return HydratedTemplate(
        TemplateProvider(template_file=DOCUMENT_TEMPLATE),
        read_template(TEMPLATES_PATH, DOCUMENT_TEMPLATE)
    )