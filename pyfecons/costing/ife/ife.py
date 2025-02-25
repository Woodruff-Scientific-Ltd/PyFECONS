from typing import Optional

from pyfecons.data import Data
from pyfecons.enums import ReactorType
from pyfecons.helpers import get_local_included_files_map
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.report import ReportContent, ReportOverrides
from pyfecons.costing_data import CostingData
from pyfecons.templates import (
    hydrate_templates,
    combine_figures,
    load_document_template,
)
from pyfecons.costing.ife.PowerBalance import power_balance
from pyfecons.costing.calculations.cas10_pre_construction import cas_10_pre_construction_costs
from pyfecons.costing.calculations.cas21_buildings import cas_21_building_costs
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
from pyfecons.costing.calculations.cas22.CAS220119 import (
    cas_220119_scheduled_replacement_cost,
)
from pyfecons.costing.ife.cas22.CAS220200 import cas_2202_main_and_secondary_coolant
from pyfecons.costing.ife.cas22.CAS220300 import cas_2203_auxilary_cooling
from pyfecons.costing.calculations.cas22.cas220400_rad_waste import cas_2204_radwaste
from pyfecons.costing.ife.cas22.CAS220500 import cas_2205_fuel_handling_and_storage
from pyfecons.costing.ife.cas22.CAS220600 import cas_2206_other_reactor_plant_equipment
from pyfecons.costing.ife.cas22.CAS220700 import cas_2207_instrumentation_and_control
from pyfecons.costing.calculations.cas22.CAS22 import (
    cas_2200_reactor_plant_equipment_total,
)
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
from pyfecons.costing.calculations.npv import calculate_npv

TEMPLATES_PATH = "pyfecons.costing.ife.templates"
INCLUDED_FILES_PATH = "pyfecons.costing.ife.included_files"
DOCUMENT_TEMPLATE = "Costing_ARPA-E_IFE_Modified.tex"

# list representing latex_path in included_files directory
LOCAL_INCLUDED_FILES = [
    "additions.bib",
    "glossary.tex",
    "IEEEtran.bst",
    "ST-SC.bib",
    "Figures/Bayrmanian2011.png",
    "Figures/FastIgnition.png",
    "Originals/CAS220100_IFE.tex",
    "Originals/method.tex",
    "Originals/powerBalanceIFEDT.tex",
    "StandardFigures/costcategories.png",
    "StandardFigures/power.eps",
    "StandardFigures/signature.jpg",
    "StandardFigures/siteplan2023.eps",
    "StandardFigures/statista.png",
    "StandardFigures/steamPbLi-eps-converted-to.pdf",
    "StandardFigures/TIsketch.eps",
    "StandardFigures/WSLTD_logo.png",
]


def GenerateCostingData(inputs: AllInputs) -> CostingData:
    data = Data(reactor_type=ReactorType.IFE)
    data.power_table = power_balance(inputs.basic, inputs.power_input)
    data.cas10 = cas_10_pre_construction_costs(inputs.basic, data.power_table)
    data.cas21 = cas_21_building_costs(inputs, data)
    data.cas220101 = cas_220101_reactor_equipment(inputs, data)
    data.cas220102 = cas_220102_shield(inputs, data)
    data.cas220103 = cas_220103_lasers(inputs, data)
    data.cas220104 = cas_220104_ignition_lasers(inputs, data)
    data.cas220105 = cas_220105_primary_structure(inputs, data)
    data.cas220106 = cas_220106_vacuum_system(inputs, data)
    data.cas220107 = cas_220107_power_supplies(inputs, data)
    data.cas220108 = cas_220108_target_factory(inputs, data)
    data.cas220109 = cas_220109_direct_energy_converter(inputs, data)
    data.cas220111 = cas_220111_installation_costs(inputs, data)
    data.cas220119 = cas_220119_scheduled_replacement_cost(inputs, data)
    data.cas2202 = cas_2202_main_and_secondary_coolant(inputs, data)
    data.cas2203 = cas_2203_auxilary_cooling(inputs, data)
    data.cas2204 = cas_2204_radwaste(data)
    data.cas2205 = cas_2205_fuel_handling_and_storage(inputs, data)
    data.cas2206 = cas_2206_other_reactor_plant_equipment(data)
    data.cas2207 = cas_2207_instrumentation_and_control(data)
    data.cas22 = cas_2200_reactor_plant_equipment_total(data)
    data.cas23 = cas_23(inputs, data)
    data.cas24 = cas_24(inputs, data)
    data.cas25 = cas_25(inputs, data)
    data.cas26 = cas_26(inputs, data)
    data.cas27 = cas_27(inputs, data)
    data.cas28 = cas_28(inputs, data)
    data.cas29 = cas_29(inputs, data)
    data.cas20 = cas_20(inputs, data)
    data.cas30 = cas_30(inputs, data)
    data.cas40 = cas_40(inputs, data)
    data.cas50 = cas_50(inputs, data)
    data.cas60 = cas_60(inputs, data)
    data.cas70 = cas_70(inputs, data)
    data.cas80 = cas_80(inputs, data)
    data.cas90 = cas_90(inputs, data)
    data.lcoe = lcoe(inputs, data)
    data.cost_table = cost_table(inputs, data)
    data.npv = calculate_npv(inputs, data)
    return CostingData(data, data.template_providers())


def CreateReportContent(
    costing_data: CostingData, overrides: Optional[ReportOverrides] = None
) -> ReportContent:
    document_template = load_document_template(
        TEMPLATES_PATH, DOCUMENT_TEMPLATE, overrides
    )
    hydrated_templates = hydrate_templates(
        TEMPLATES_PATH, costing_data.template_providers, overrides
    )
    figures = combine_figures(costing_data.template_providers)
    included_files = get_local_included_files_map(
        INCLUDED_FILES_PATH, LOCAL_INCLUDED_FILES, overrides
    )
    return ReportContent(document_template, hydrated_templates, included_files, figures)
