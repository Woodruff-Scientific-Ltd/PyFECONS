from pyfecons.helpers import load_remote_included_files, load_github_images
from pyfecons.templates import read_template, hydrate_templates, combine_figures
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.costing.mfe.PowerBalance import power_balance
from pyfecons.costing.mfe.CAS10 import cas_10
from pyfecons.costing.mfe.CAS21 import cas_21
from pyfecons.costing.mfe.cas22.CAS220101 import cas_220101_reactor_equipment
from pyfecons.costing.mfe.cas22.CAS220102 import cas_220102_shield
from pyfecons.costing.mfe.cas22.CAS220103 import cas_220103_coils
from pyfecons.costing.mfe.cas22.CAS220104 import cas_220104_supplementary_heating
from pyfecons.costing.mfe.cas22.CAS220105 import cas_220105_primary_structure
from pyfecons.costing.mfe.cas22.CAS220106 import cas_220106_vacuum_system
from pyfecons.costing.mfe.cas22.CAS220107 import cas_220107_power_supplies
from pyfecons.costing.mfe.cas22.CAS220108 import cas_220108_divertor
from pyfecons.costing.mfe.cas22.CAS220109 import cas_220109_direct_energy_converter
from pyfecons.costing.mfe.cas22.CAS220111 import cas_220111_installation_costs
from pyfecons.costing.mfe.cas22.CAS220119 import cas_220119_scheduled_replacement_cost
from pyfecons.costing.mfe.cas22.CAS2202 import cas_2202_main_and_secondary_coolant
from pyfecons.costing.mfe.cas22.CAS2203 import cas_2203_auxilary_cooling
from pyfecons.costing.mfe.cas22.CAS2204 import cas_2204_radwaste
from pyfecons.costing.mfe.cas22.CAS2205 import cas_2205_fuel_handling_and_storage
from pyfecons.costing.mfe.cas22.CAS2206 import cas_2206_other_reactor_plant_equipment
from pyfecons.costing.mfe.cas22.CAS2207 import cas_2207_instrumentation_and_control
from pyfecons.costing.mfe.cas22.CAS22 import cas_2200_reactor_plant_equipment_total
from pyfecons.costing.mfe.CAS23 import cas_23
from pyfecons.costing.mfe.CAS24 import cas_24
from pyfecons.costing.mfe.CAS25 import cas_25
from pyfecons.costing.mfe.CAS26 import cas_26
from pyfecons.costing.mfe.CAS27 import cas_27
from pyfecons.costing.mfe.CAS28 import cas_28
from pyfecons.costing.mfe.CAS29 import cas_29
from pyfecons.costing.mfe.CAS20 import cas_20
from pyfecons.costing.mfe.CAS30 import cas_30
from pyfecons.costing.mfe.CAS40 import cas_40
from pyfecons.costing.mfe.CAS50 import cas_50
from pyfecons.costing.mfe.CAS60 import cas_60
from pyfecons.costing.mfe.CAS70 import cas_70
from pyfecons.costing.mfe.CAS80 import cas_80
from pyfecons.costing.mfe.CAS90 import cas_90
from pyfecons.costing.mfe.LCOE import lcoe
from pyfecons.costing.mfe.CostTable import cost_table
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
    template_providers = [
        power_balance(inputs, data),
        cas_10(inputs, data),
        cas_21(inputs, data),
        cas_220101_reactor_equipment(inputs, data),
        cas_220102_shield(inputs, data),
        cas_220103_coils(inputs, data),
        cas_220104_supplementary_heating(inputs, data),
        cas_220105_primary_structure(inputs, data),
        cas_220106_vacuum_system(inputs, data),
        cas_220107_power_supplies(inputs, data),
        cas_220108_divertor(inputs, data),
        cas_220109_direct_energy_converter(inputs, data),
        cas_220111_installation_costs(inputs, data),
        cas_220119_scheduled_replacement_cost(data),
        cas_2202_main_and_secondary_coolant(inputs, data),
        cas_2203_auxilary_cooling(inputs, data),
        cas_2204_radwaste(data),
        cas_2205_fuel_handling_and_storage(inputs, data),
        cas_2206_other_reactor_plant_equipment(data),
        cas_2207_instrumentation_and_control(data),
        cas_2200_reactor_plant_equipment_total(inputs, data),
        cas_23(inputs, data),
        cas_24(inputs, data),
        cas_25(inputs, data),
        cas_26(inputs, data),
        cas_27(inputs, data),
        cas_28(inputs, data),
        cas_29(inputs, data),
        cas_20(inputs, data),
        cas_30(inputs, data),
        cas_40(inputs, data),
        cas_50(inputs, data),
        cas_60(inputs, data),
        cas_70(inputs, data),
        cas_80(inputs, data),
        cas_90(inputs, data),
        lcoe(inputs, data),
        cost_table(inputs, data),
    ]
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
