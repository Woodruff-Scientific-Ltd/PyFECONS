from pyfecons.enums import ReactorType
from pyfecons.helpers import get_local_included_files_map
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
from pyfecons.costing.mfe.cas22.CAS220200 import cas_2202_main_and_secondary_coolant
from pyfecons.costing.mfe.cas22.CAS220300 import cas_2203_auxilary_cooling
from pyfecons.costing.mfe.cas22.CAS220400 import cas_2204_radwaste
from pyfecons.costing.mfe.cas22.CAS220500 import cas_2205_fuel_handling_and_storage
from pyfecons.costing.mfe.cas22.CAS220600 import cas_2206_other_reactor_plant_equipment
from pyfecons.costing.mfe.cas22.CAS220700 import cas_2207_instrumentation_and_control
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
INCLUDED_FILES_PATH = 'pyfecons.costing.mfe.included_files'

LOCAL_INCLUDED_FILES = {
    'ST-SC.bib': 'ST-SC.bib',
    'additions.bib': 'additions.bib',
    'glossary.tex': 'glossary.tex',
    'IEEEtran.bst': 'IEEEtran.bst',
    'Figures/cooling_efficiency.pdf': 'Figures/cooling_efficiency.pdf',
    'Figures/MFE.png': 'Figures/MFE.png',
    'Originals/CAS220100_MFE.tex': 'Originals/CAS220100_MFE.tex',
    'Originals/method.tex': 'Originals/method.tex',
    'Originals/powerBalanceMFEDT.tex': 'Originals/powerBalanceMFEDT.tex',
    'StandardFigures/TIsketch.eps': 'StandardFigures/TIsketch.eps',
    'StandardFigures/WSLTD_logo.png': 'StandardFigures/WSLTD_logo.png',
    'StandardFigures/costcategories.png': 'StandardFigures/costcategories.png',
    'StandardFigures/power.eps': 'StandardFigures/power.eps',
    'StandardFigures/signature.jpg': 'StandardFigures/signature.jpg',
    'StandardFigures/siteplan2023.eps': 'StandardFigures/siteplan2023.eps',
    'StandardFigures/statista.png': 'StandardFigures/statista.png',
    'StandardFigures/steamPbLi-eps-converted-to.pdf': 'StandardFigures/steamPbLi-eps-converted-to.pdf',
    'StandardFigures/yuhu_cs.pdf': 'StandardFigures/yuhu_cs.pdf',
}

def GenerateCostingData(inputs: Inputs) -> CostingData:
    data = Data(reactor_type=ReactorType.MFE)
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
    included_files = get_local_included_files_map(INCLUDED_FILES_PATH, LOCAL_INCLUDED_FILES)
    return ReportContent(document_template, hydrated_templates, included_files, figures)
