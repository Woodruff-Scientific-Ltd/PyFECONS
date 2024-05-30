from pyfecons.data import Data, TemplateProvider
from pyfecons.enums import ReactorType
from pyfecons.helpers import get_local_included_files_map
from pyfecons.inputs import Inputs
from pyfecons.report import CostingData, ReportContent, HydratedTemplate
from pyfecons.templates import read_template, hydrate_templates, combine_figures
from pyfecons.costing.ife.PowerBalance import power_balance
from pyfecons.costing.ife.CAS10 import cas_10
from pyfecons.costing.ife.CAS21 import cas_21
from pyfecons.costing.ife.cas22.CAS220101 import cas_220101_reactor_equipment
from pyfecons.costing.ife.cas22.CAS220102 import cas_220102_shield
from pyfecons.costing.ife.cas22.CAS220103 import cas_220103_lasers
from pyfecons.costing.ife.cas22.CAS220104 import cas_220104_ignition_lasers
from pyfecons.costing.ife.cas22.CAS220105 import cas_220105_primary_structure
from pyfecons.costing.ife.cas22.CAS220106 import cas_220106_vacuum_system
from pyfecons.costing.ife.cas22.CAS220107 import cas_220107_power_supplies
from pyfecons.costing.ife.cas22.CAS220108 import cas_220108_target_factory
from pyfecons.costing.ife.cas22.CAS220109 import cas_220109_direct_energy_converter
from pyfecons.costing.ife.cas22.CAS220111 import cas_220111_installation_costs
from pyfecons.costing.ife.cas22.CAS220119 import cas_220119_scheduled_replacement_cost
from pyfecons.costing.ife.cas22.CAS220200 import cas_2202_main_and_secondary_coolant
from pyfecons.costing.ife.cas22.CAS220300 import cas_2203_auxilary_cooling
from pyfecons.costing.ife.cas22.CAS220400 import cas_2204_radwaste
from pyfecons.costing.ife.cas22.CAS220500 import cas_2205_fuel_handling_and_storage
from pyfecons.costing.ife.cas22.CAS220600 import cas_2206_other_reactor_plant_equipment
from pyfecons.costing.ife.cas22.CAS220700 import cas_2207_instrumentation_and_control
from pyfecons.costing.ife.CAS23 import cas_23
from pyfecons.costing.ife.CAS24 import cas_24
from pyfecons.costing.ife.CAS25 import cas_25
from pyfecons.costing.ife.CAS26 import cas_26
from pyfecons.costing.ife.CAS27 import cas_27
from pyfecons.costing.ife.CAS28 import cas_28
from pyfecons.costing.ife.CAS29 import cas_29
from pyfecons.costing.ife.CAS20 import cas_20
from pyfecons.costing.ife.CAS30 import cas_30
from pyfecons.costing.ife.CAS40 import cas_40
from pyfecons.costing.ife.CAS50 import cas_50
from pyfecons.costing.ife.CAS60 import cas_60
from pyfecons.costing.ife.CAS70 import cas_70
from pyfecons.costing.ife.CAS80 import cas_80
from pyfecons.costing.ife.CAS90 import cas_90
from pyfecons.costing.ife.CostTable import cost_table
from pyfecons.costing.ife.LCOE import lcoe

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
    'StandardFigures/TIsketch.eps': 'TIsketch.eps',
    'StandardFigures/statista.png': 'statista.png',
    'Figures/Bayrmanian2011.png': 'Bayrmanian2011.png',
    'StandardFigures/steamPbLi-eps-converted-to.pdf': 'StandardFigures/steamPbLi-eps-converted-to.pdf',
}


def GenerateCostingData(inputs: Inputs) -> CostingData:
    data = Data(reactor_type=ReactorType.IFE)
    template_providers = [
        power_balance(inputs, data),
        cas_10(inputs, data),
        cas_220101_reactor_equipment(inputs, data),
        cas_220102_shield(inputs, data),
        cas_220103_lasers(inputs, data),
        cas_220104_ignition_lasers(inputs, data),
        cas_220105_primary_structure(inputs, data),
        cas_220106_vacuum_system(inputs, data),
        cas_220107_power_supplies(inputs, data),
        cas_220108_target_factory(inputs, data),
        cas_220109_direct_energy_converter(inputs, data),
        cas_220111_installation_costs(inputs, data),
        cas_220119_scheduled_replacement_cost(data),
        cas_2202_main_and_secondary_coolant(inputs, data),
        cas_2203_auxilary_cooling(inputs, data),
        cas_2204_radwaste(data),
        cas_2205_fuel_handling_and_storage(inputs, data),
        cas_2206_other_reactor_plant_equipment(data),
        cas_2207_instrumentation_and_control(data),
        cas_21(inputs, data),
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
        cost_table(inputs, data),
        lcoe(inputs, data),
    ]
    return CostingData(data, template_providers)


def CreateReportContent(costing_data: CostingData) -> ReportContent:
    document_template = load_document_template()
    hydrated_templates = hydrate_templates(TEMPLATES_PATH, costing_data.template_providers)
    figures = combine_figures(costing_data.template_providers)
    included_files = get_local_included_files_map(INCLUDED_FILES_PATH, LOCAL_INCLUDED_FILES)
    return ReportContent(document_template, hydrated_templates, included_files, figures)


def load_document_template() -> HydratedTemplate:
    return HydratedTemplate(
        TemplateProvider(template_file=DOCUMENT_TEMPLATE),
        read_template(TEMPLATES_PATH, DOCUMENT_TEMPLATE)
    )