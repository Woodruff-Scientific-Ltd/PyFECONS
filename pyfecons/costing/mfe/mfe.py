from typing import Optional

from pyfecons.enums import ReactorType
from pyfecons.helpers import get_local_included_files_map
from pyfecons.templates import (
    hydrate_templates,
    combine_figures,
    load_document_template,
)
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.costing_data import CostingData
from pyfecons.costing.mfe.PowerBalance import power_balance
from pyfecons.costing.calculations.cas10_pre_construction import (
    cas_10_pre_construction_costs,
)
from pyfecons.costing.calculations.cas21_buildings import cas_21_building_costs
from pyfecons.costing.calculations.cas22.cas220101_reactor_equipment import (
    cas_220101_reactor_equipment_costs,
)
from pyfecons.costing.calculations.cas22.cas220102_shield import cas_220102_shield_costs
from pyfecons.costing.mfe.cas22.cas220103_coils import cas_220103_coils
from pyfecons.costing.mfe.cas22.cas220104_supplementary_heating import (
    cas_220104_supplementary_heating_costs,
)
from pyfecons.costing.calculations.cas22.cas220105_primary_structure import (
    cas_220105_primary_structure_costs,
)
from pyfecons.costing.mfe.cas22.cas220106_vacuum_system import (
    cas_220106_vacuum_system_costs,
)
from pyfecons.costing.mfe.cas22.cas220107_power_supplies import (
    cas_220107_power_supply_costs,
)
from pyfecons.costing.mfe.cas22.cas220108_divertor import cas_220108_divertor_costs
from pyfecons.costing.calculations.cas22.cas220109_direct_energy_converter import (
    cas_220109_direct_energy_converter_costs,
)
from pyfecons.costing.calculations.cas22.cas220111_installation import (
    cas_220111_installation_costs,
)
from pyfecons.costing.calculations.cas22.cas220119_replacement import (
    cas_220119_scheduled_replacement_costs,
)
from pyfecons.costing.calculations.cas22.cas220200_coolant import (
    cas_2202_main_and_secondary_coolant_costs,
)
from pyfecons.costing.calculations.cas22.cas220300_auxilary_cooling import (
    cas_2203_auxilary_cooling_costs,
)
from pyfecons.costing.calculations.cas22.cas220400_rad_waste import (
    cas_2204_radwaste_costs,
)
from pyfecons.costing.calculations.cas22.cas220500_fuel_handling_and_storage import (
    cas_2205_fuel_handling_and_storage_costs,
)
from pyfecons.costing.calculations.cas22.cas220600_other_plant_equipment import (
    cas_2206_other_reactor_plant_equipment_costs,
)
from pyfecons.costing.calculations.cas22.cas220700_instrumentation_and_control import (
    cas_2207_instrumentation_and_control_costs,
)
from pyfecons.costing.calculations.cas22.cas22_reactor_plant_equipment_total import (
    cas22_reactor_plant_equipment_total_costs,
)
from pyfecons.costing.calculations.cas23_turbine_plant_equipment import (
    cas23_turbine_plant_equipment_costs,
)
from pyfecons.costing.calculations.cas24_electric_plant_equipment import (
    cas24_electric_plant_equipment_costs,
)
from pyfecons.costing.calculations.cas25_misc_plant_equipment import (
    cas25_misc_plant_equipment_costs,
)
from pyfecons.costing.calculations.cas26_heat_rejection import (
    cas26_heat_rejection_costs,
)
from pyfecons.costing.calculations.cas27_special_materials import (
    cas27_special_materials_costs,
)
from pyfecons.costing.calculations.cas28_digital_twin import cas28_digital_twin_costs
from pyfecons.costing.calculations.cas29_contingency import cas29_contingency_costs
from pyfecons.costing.calculations.cas20_total_costs import cas20_total_costs
from pyfecons.costing.calculations.cas30_capitalized_indirect_service import (
    cas30_capitalized_indirect_service_costs,
)
from pyfecons.costing.calculations.cas40_capitalized_owner import (
    cas40_capitalized_owner_costs,
)
from pyfecons.costing.calculations.cas50_capitalized_supplementary import (
    cas50_capitalized_supplementary_costs,
)
from pyfecons.costing.calculations.cas60_capitalized_financial import (
    cas60_capitalized_financial_costs,
)
from pyfecons.costing.calculations.cas70_annualized_om import cas70_annualized_om_costs
from pyfecons.costing.mfe.cas80_annualized_fuel import cas80_annualized_fuel_costs
from pyfecons.costing.calculations.cas90_annualized_financial import (
    cas90_annualized_financial_costs,
)
from pyfecons.costing.calculations.lcoe import lcoe_costs
from pyfecons.costing.mfe.cost_table import cost_table
from pyfecons.costing.calculations.npv import calculate_npv
from pyfecons.report import ReportContent, ReportOverrides

TEMPLATES_PATH = "pyfecons.costing.mfe.templates"
INCLUDED_FILES_PATH = "pyfecons.costing.mfe.included_files"
DOCUMENT_TEMPLATE = "Costing_ARPA-E_MFE_Modified.tex"

# list representing latex_path in included_files directory
LOCAL_INCLUDED_FILES = [
    "additions.bib",
    "glossary.tex",
    "IEEEtran.bst",
    "ST-SC.bib",
    "Figures/cooling_efficiency.pdf",
    "Figures/MFE.png",
    "Originals/CAS220100_MFE.tex",
    "Originals/method.tex",
    "Originals/powerBalanceMFEDT.tex",
    "StandardFigures/TIsketch.eps",
    "StandardFigures/WSLTD_logo.png",
    "StandardFigures/costcategories.png",
    "StandardFigures/power.eps",
    "StandardFigures/signature.jpg",
    "StandardFigures/siteplan2023.eps",
    "StandardFigures/statista.png",
    "StandardFigures/steamPbLi-eps-converted-to.pdf",
    "StandardFigures/yuhu_cs.pdf",
]


def GenerateCostingData(inputs: AllInputs) -> CostingData:
    data = CostingData(reactor_type=ReactorType.MFE)
    data.power_table = power_balance(inputs.basic, inputs.power_input)
    data.cas10 = cas_10_pre_construction_costs(inputs.basic, data.power_table)
    data.cas21 = cas_21_building_costs(inputs.basic, data.power_table)
    data.cas220101 = cas_220101_reactor_equipment_costs(
        inputs.basic, inputs.radial_build, inputs.blanket
    )
    data.cas220102 = cas_220102_shield_costs(
        inputs.basic, inputs.shield, inputs.blanket, data.cas220101
    )
    data.cas220103 = cas_220103_coils(
        inputs.coils, inputs.radial_build, data.power_table
    )
    data.cas220104 = cas_220104_supplementary_heating_costs(
        inputs.supplementary_heating
    )
    data.cas220105 = cas_220105_primary_structure_costs(
        inputs.basic, inputs.primary_structure, data.power_table
    )
    data.cas220106 = cas_220106_vacuum_system_costs(
        inputs.vacuum_system,
        inputs.radial_build,
        inputs.coils,
        data.power_table,
        data.cas220101,
    )
    data.cas220107 = cas_220107_power_supply_costs(
        inputs.basic, inputs.power_supplies, data.power_table
    )
    data.cas220108 = cas_220108_divertor_costs(data.cas220101)
    data.cas220109 = cas_220109_direct_energy_converter_costs(
        inputs.basic, inputs.direct_energy_converter
    )
    data.cas220111 = cas_220111_installation_costs(
        inputs.basic, inputs.installation, data.cas220101
    )
    data.cas220119 = cas_220119_scheduled_replacement_costs(
        inputs.primary_structure, data.cas2201_total_cost()
    )
    data.cas2202 = cas_2202_main_and_secondary_coolant_costs(
        inputs.basic, inputs.blanket, data.power_table
    )
    data.cas2203 = cas_2203_auxilary_cooling_costs(inputs.basic, data.power_table)
    data.cas2204 = cas_2204_radwaste_costs(data.power_table)
    data.cas2205 = cas_2205_fuel_handling_and_storage_costs(inputs.fuel_handling)
    data.cas2206 = cas_2206_other_reactor_plant_equipment_costs(data.power_table)
    data.cas2207 = cas_2207_instrumentation_and_control_costs()
    data.cas22 = cas22_reactor_plant_equipment_total_costs(
        data.cas2201_total_cost(), data.cas2200_total_cost()
    )
    data.cas23 = cas23_turbine_plant_equipment_costs(inputs.basic, data.power_table)
    data.cas24 = cas24_electric_plant_equipment_costs(inputs.basic, data.power_table)
    data.cas25 = cas25_misc_plant_equipment_costs(inputs.basic, data.power_table)
    data.cas26 = cas26_heat_rejection_costs(inputs.basic, data.power_table)
    data.cas27 = cas27_special_materials_costs(inputs.blanket, data.cas220101)
    data.cas28 = cas28_digital_twin_costs()
    data.cas29 = cas29_contingency_costs(inputs.basic, data.cas2x_total_cost())
    data.cas20 = cas20_total_costs(data.cas2x_total_cost())
    data.cas30 = cas30_capitalized_indirect_service_costs(
        inputs.basic, inputs.lsa_levels, data.power_table, data.cas20
    )
    data.cas40 = cas40_capitalized_owner_costs(inputs.lsa_levels, data.cas20)
    data.cas50 = cas50_capitalized_supplementary_costs(
        inputs.basic, data.power_table, data.cas23_to_28_total_cost()
    )
    data.cas60 = cas60_capitalized_financial_costs(
        inputs.basic, inputs.financial, inputs.lsa_levels, data.power_table, data.cas20
    )
    data.cas70 = cas70_annualized_om_costs(data.power_table)
    data.cas80 = cas80_annualized_fuel_costs(inputs.basic, inputs.blanket)
    data.cas90 = cas90_annualized_financial_costs(
        inputs.financial, data.cas10_to_60_total_capital_cost()
    )
    data.lcoe = lcoe_costs(
        inputs.basic, data.power_table, data.cas70, data.cas80, data.cas90
    )
    data.cost_table = cost_table(data)
    data.npv = calculate_npv(inputs.basic, inputs.npv_input, data)
    return data


def CreateReportContent(
    costing_data: CostingData, overrides: Optional[ReportOverrides] = None
) -> ReportContent:
    document_template = load_document_template(
        TEMPLATES_PATH, DOCUMENT_TEMPLATE, overrides
    )
    hydrated_templates = hydrate_templates(
        TEMPLATES_PATH, costing_data.template_providers(), overrides
    )
    figures = combine_figures(costing_data.template_providers())
    included_files = get_local_included_files_map(
        INCLUDED_FILES_PATH, LOCAL_INCLUDED_FILES, overrides
    )
    return ReportContent(document_template, hydrated_templates, included_files, figures)
