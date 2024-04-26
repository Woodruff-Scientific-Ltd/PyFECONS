from pyfecons.helpers import load_remote_included_files, load_github_images
from pyfecons.templates import read_template, hydrate_templates, combine_figures
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.costing.mfe.PowerBalance import GenerateData as PowerBalanceData
from pyfecons.costing.mfe.CAS10 import GenerateData as CAS10Data
from pyfecons.costing.mfe.CAS21 import GenerateData as CAS21Data
from pyfecons.costing.mfe.CAS22 import GenerateData as CAS22Data
from pyfecons.costing.mfe.CAS23 import GenerateData as CAS23Data
from pyfecons.costing.mfe.CAS24 import GenerateData as CAS24Data
from pyfecons.costing.mfe.CAS25 import GenerateData as CAS25Data
from pyfecons.costing.mfe.CAS26 import GenerateData as CAS26Data
from pyfecons.costing.mfe.CAS27 import GenerateData as CAS27Data
from pyfecons.costing.mfe.CAS28 import GenerateData as CAS28Data
from pyfecons.costing.mfe.CAS29 import GenerateData as CAS29Data
from pyfecons.costing.mfe.CAS20 import GenerateData as CAS20Data
from pyfecons.costing.mfe.CAS30 import GenerateData as CAS30Data
from pyfecons.costing.mfe.CAS40 import GenerateData as CAS40Data
from pyfecons.costing.mfe.CAS50 import GenerateData as CAS50Data
from pyfecons.costing.mfe.CAS60 import GenerateData as CAS60Data
from pyfecons.costing.mfe.CAS70 import GenerateData as CAS70Data
from pyfecons.costing.mfe.CAS80 import GenerateData as CAS80Data
from pyfecons.costing.mfe.CAS90 import GenerateData as CAS90Data
from pyfecons.costing.mfe.LCOE import GenerateData as LCOEData
from pyfecons.costing.mfe.CostTable import GenerateData as CostTableData
from pyfecons.report import ReportContent, CostingData, HydratedTemplate

TEMPLATES_PATH = 'pyfecons.costing.mfe.templates'
DOCUMENT_TEMPLATE = 'Costing_ARPA-E_MFE_Modified.tex'
BASE_URL = 'https://raw.githubusercontent.com/Woodruff-Scientific-Ltd/PyFECONS/'
CACHE = 'temp/cache/mfe'
# GitHub files to include in the tex compilation: tex file path -> remote path
INCLUDED_FILES = {
    'ST-SC.bib': '884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/ST-SC.bib',
    'additions.bib': '884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/additions.bib',
    'glossary.tex': '884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/glossary.tex',
    'IEEEtran.bst': '884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/IEEEtran.bst',
    'Originals/method.tex': '884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/Originals/method.tex',
    'Originals/powerBalanceMFEDT.tex': '884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/Originals/powerBalanceMFEDT.tex',
    'StandardFigures/power.eps': '884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/StandardFigures/power.eps',
    'Originals/CAS220100_MFE.tex': '884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/Originals/CAS220100_MFE.tex',
    'StandardFigures/siteplan2023.eps': '884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/StandardFigures/siteplan2023.eps',
    'StandardFigures/TIsketch.eps': '884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/StandardFigures/TIsketch.eps',
}
# GitHub images to include in the tex compilation: tex file path -> remote path
INCLUDED_IMAGES = {
    'Figures/MFE.png': 'https://github.com/Woodruff-Scientific-Ltd/PyFECONS/blob/884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/Figures/MFE.png?raw=true',
    'StandardFigures/WSLTD_logo.png': 'https://github.com/Woodruff-Scientific-Ltd/PyFECONS/blob/884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/StandardFigures/WSLTD_logo.png?raw=true',
    'StandardFigures/signature.jpg': 'https://github.com/Woodruff-Scientific-Ltd/PyFECONS/blob/884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/StandardFigures/signature.jpg?raw=true',
    'StandardFigures/costcategories.png': 'https://github.com/Woodruff-Scientific-Ltd/PyFECONS/blob/884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/StandardFigures/costcategories.png?raw=true',
    'StandardFigures/yuhu_cs.pdf': 'https://github.com/Woodruff-Scientific-Ltd/PyFECONS/blob/884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/StandardFigures/yuhu_cs.pdf?raw=true',
    'Figures/cooling_efficiency.pdf': 'https://github.com/Woodruff-Scientific-Ltd/PyFECONS/blob/884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/Figures/cooling_efficiency.pdf?raw=true',
    'StandardFigures/steamPbLi-eps-converted-to.pdf': 'https://github.com/Woodruff-Scientific-Ltd/PyFECONS/blob/884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/StandardFigures/steamPbLi-eps-converted-to.pdf?raw=true',
    'StandardFigures/statista.png': 'https://github.com/Woodruff-Scientific-Ltd/PyFECONS/blob/884a3f842f0e5027e0c8e20591624d6251cc399f/MFE/StandardFigures/statista.png?raw=true',
}


def GenerateCostingData(inputs: Inputs) -> CostingData:
    data = Data()
    figures = {}
    template_providers = (
            PowerBalanceData(inputs, data, figures)
            + CAS10Data(inputs, data, figures)
            + CAS21Data(inputs, data, figures)
            + CAS22Data(inputs, data, figures)
            + CAS23Data(inputs, data, figures)
            + CAS24Data(inputs, data, figures)
            + CAS25Data(inputs, data, figures)
            + CAS26Data(inputs, data, figures)
            + CAS27Data(inputs, data, figures)
            + CAS28Data(inputs, data, figures)
            + CAS29Data(inputs, data, figures)
            + CAS20Data(inputs, data, figures)
            + CAS30Data(inputs, data, figures)
            + CAS40Data(inputs, data, figures)
            + CAS50Data(inputs, data, figures)
            + CAS60Data(inputs, data, figures)
            + CAS70Data(inputs, data, figures)
            + CAS80Data(inputs, data, figures)
            + CAS90Data(inputs, data, figures)
            + LCOEData(inputs, data, figures)
            + CostTableData(inputs, data, figures)
    )
    return CostingData(data, template_providers)


def load_document_template() -> HydratedTemplate:
    return HydratedTemplate(
        TemplateProvider(template_file=DOCUMENT_TEMPLATE),
        read_template(TEMPLATES_PATH, DOCUMENT_TEMPLATE)
    )


def CreateReportContent(costing_data: CostingData) -> ReportContent:
    document_template = load_document_template()
    hydrated_templates = hydrate_templates(TEMPLATES_PATH, costing_data.template_providers)
    figures = combine_figures(costing_data.template_providers)
    included_files = load_remote_included_files(CACHE, BASE_URL, INCLUDED_FILES)
    included_files = included_files | load_github_images(CACHE, INCLUDED_IMAGES)
    return ReportContent(document_template, hydrated_templates, included_files, figures)
