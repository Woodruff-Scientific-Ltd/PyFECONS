from importlib import resources

from pyfecons.inputs import Inputs, Blanket
from pyfecons.data import Data, CAS80
from pyfecons.costing.mfe.PowerBalance import GenerateData as PowerBalanceData, POWER_TABLE_MFE_DT_TEX
from pyfecons.costing.mfe.CAS10 import GenerateData as CAS10Data, CAS_100000_TEX
from pyfecons.costing.mfe.CAS21 import GenerateData as CAS21Data, CAS_210000_TEX
from pyfecons.costing.mfe.CAS22 import (GenerateData as CAS22Data, CAS_220101_MFE_DT_TEX, CAS_220102_TEX
, CAS_220103_MIF_DT_MIRROR, CAS_220104_MFE_DT, CAS_220105_TEX, CAS_220106_MFE_TEX, CAS_220107_MFE_TEX
, CAS_220108_MFE_TEX, CAS_220109_TEX, CAS_220111_TEX, CAS_220119_TEX, CAS_220200_DT_TEX, CAS_220300_TEX, CAS_220400_TEX
, CAS_220500_DT_TEX, CAS_220600_TEX, CAS_220700_TEX, CAS_220000_TEX)
from pyfecons.costing.mfe.CAS23 import GenerateData as CAS23Data, CAS_230000_TEX
from pyfecons.costing.mfe.CAS24 import GenerateData as CAS24Data, CAS_240000_TEX
from pyfecons.costing.mfe.CAS25 import GenerateData as CAS25Data, CAS_250000_TEX
from pyfecons.costing.mfe.CAS26 import GenerateData as CAS26Data, CAS_260000_TEX
from pyfecons.costing.mfe.CAS27 import GenerateData as CAS27Data, CAS_270000_TEX
from pyfecons.costing.mfe.CAS28 import GenerateData as CAS28Data, CAS_280000_TEX
from pyfecons.costing.mfe.CAS29 import GenerateData as CAS29Data, CAS_290000_TEX
from pyfecons.costing.mfe.CAS20 import GenerateData as CAS20Data, CAS_200000_TEX
from pyfecons.costing.mfe.CAS30 import GenerateData as CAS30Data, CAS_300000_TEX
from pyfecons.costing.mfe.CAS40 import GenerateData as CAS40Data, CAS_400000_TEX
from pyfecons.costing.mfe.CAS50 import GenerateData as CAS50Data, CAS_500000_TEX
from pyfecons.costing.mfe.CAS60 import GenerateData as CAS60Data, CAS_600000_TEX
from pyfecons.costing.mfe.CAS70 import GenerateData as CAS70Data, CAS_700000_TEX
from pyfecons.costing.mfe.CAS80 import GenerateData as CAS80Data
from pyfecons.costing.mfe.CAS90 import GenerateData as CAS90Data
from pyfecons.costing.mfe.LCOE import GenerateData as LCOEData
from pyfecons.costing.mfe.CostTable import GenerateData as CostTableData, CAS_STRUCTURE_TEX

CAS_800000_DT_TEX = 'CAS800000_DT.tex'
CAS_900000_TEX = 'CAS900000.tex'
LCOE_TEX = 'LCOE.tex'

TEMPLATE_FILES = [
    POWER_TABLE_MFE_DT_TEX,
    CAS_100000_TEX,
    CAS_200000_TEX,
    CAS_210000_TEX,
    CAS_220101_MFE_DT_TEX,
    CAS_220102_TEX,
    CAS_220103_MIF_DT_MIRROR,
    CAS_220104_MFE_DT,
    CAS_220105_TEX,
    CAS_220106_MFE_TEX,
    CAS_220107_MFE_TEX,
    CAS_220108_MFE_TEX,
    CAS_220109_TEX,
    CAS_220111_TEX,
    CAS_220119_TEX,
    CAS_220200_DT_TEX,
    CAS_220300_TEX,
    CAS_220400_TEX,
    CAS_220500_DT_TEX,
    CAS_220600_TEX,
    CAS_220700_TEX,
    CAS_220000_TEX,
    CAS_230000_TEX,
    CAS_240000_TEX,
    CAS_250000_TEX,
    CAS_260000_TEX,
    CAS_270000_TEX,
    CAS_280000_TEX,
    CAS_290000_TEX,
    CAS_300000_TEX,
    CAS_400000_TEX,
    CAS_500000_TEX,
    CAS_600000_TEX,
    CAS_700000_TEX,
    CAS_800000_DT_TEX,
    CAS_900000_TEX,
    LCOE_TEX,
    CAS_STRUCTURE_TEX,
]


def GenerateData(inputs: Inputs) -> Data:
    data = Data()
    figures = {}
    PowerBalanceData(inputs, data, figures)
    CAS10Data(inputs, data, figures)
    CAS21Data(inputs, data, figures)
    CAS22Data(inputs, data, figures)
    CAS23Data(inputs, data, figures)
    CAS24Data(inputs, data, figures)
    CAS25Data(inputs, data, figures)
    CAS26Data(inputs, data, figures)
    CAS27Data(inputs, data, figures)
    CAS28Data(inputs, data, figures)
    CAS29Data(inputs, data, figures)
    CAS20Data(inputs, data, figures)
    CAS30Data(inputs, data, figures)
    CAS40Data(inputs, data, figures)
    CAS50Data(inputs, data, figures)
    CAS60Data(inputs, data, figures)
    CAS70Data(inputs, data, figures)
    CAS80Data(inputs, data, figures)
    CAS90Data(inputs, data, figures)
    LCOEData(inputs, data, figures)
    CostTableData(inputs, data, figures)
    return data


def HydrateTemplates(inputs: Inputs, data: Data) -> dict[str, str]:
    hydrated_templates = {}
    for template in TEMPLATE_FILES:
        template_content = read_template(template)
        replacements = get_template_replacements(template, inputs, data)
        hydrated_templates[template] = replace_values(template_content, replacements)
    return hydrated_templates


def read_template(template_file: str) -> str:
    with resources.path('pyfecons.costing.mfe.templates', template_file) as template_path:
        with open(template_path, 'r') as file:
            template_content = file.read()
    return template_content


def compute_cas_800000_replacements(blanket: Blanket, cas80: CAS80) -> dict[str, str]:
    return {
        'C800000': str(cas80.C800000),
        'primaryC': blanket.primary_coolant.display_name,
        'secondaryC': blanket.secondary_coolant.display_name,
    }


def compute_lcoe_replacements(inputs: Inputs, data: Data) -> dict[str, str]:
    return {
        'C1000000': str(round(data.lcoe.C1000000, 1)),
        'C2000000': str(round(data.lcoe.C2000000, 1)),
        'C700000': str(round(data.cas70.C700000, 1)),
        'C800000': str(round(data.cas80.C800000, 1)),
        'C900000': str(round(data.cas90.C900000, 1)),
        'PNET': str(round(data.power_table.p_net, 3)),
        'lifeY': str(round(inputs.basic.plant_lifetime)),
        'yinflation': str(100 * round(inputs.basic.yearly_inflation, 3)),
        'PAVAIL': str(round(inputs.basic.plant_availability, 2)),
    }


def get_template_replacements(template: str, inputs: Inputs, data: Data) -> dict[str, str]:
    if template == POWER_TABLE_MFE_DT_TEX:
        return data.power_table.replacements
    elif template == CAS_100000_TEX:
        return data.cas10.replacements
    elif template == CAS_200000_TEX:
        return data.cas20.replacements
    elif template == CAS_210000_TEX:
        return data.cas21.replacements
    elif template == CAS_220101_MFE_DT_TEX:
        return data.cas220101.replacements
    elif template == CAS_220102_TEX:
        return data.cas220102.replacements
    elif template == CAS_220103_MIF_DT_MIRROR:
        return data.cas220103.replacements
    elif template == CAS_220104_MFE_DT:
        return data.cas220104.replacements
    elif template == CAS_220105_TEX:
        return data.cas220105.replacements
    elif template == CAS_220106_MFE_TEX:
        return data.cas220106.replacements
    elif template == CAS_220107_MFE_TEX:
        return data.cas220107.replacements
    elif template == CAS_220108_MFE_TEX:
        return data.cas220108.replacements
    elif template == CAS_220109_TEX:
        return data.cas220109.replacements
    elif template == CAS_220111_TEX:
        return data.cas220111.replacements
    elif template == CAS_220119_TEX:
        return data.cas220119.replacements
    elif template == CAS_220200_DT_TEX:
        return data.cas2202.replacements
    elif template == CAS_220300_TEX:
        return data.cas2203.replacements
    elif template == CAS_220400_TEX:
        return data.cas2204.replacements
    elif template == CAS_220500_DT_TEX:
        return data.cas2205.replacements
    elif template == CAS_220600_TEX:
        return data.cas2206.replacements
    elif template == CAS_220700_TEX:
        return data.cas2207.replacements
    elif template == CAS_220000_TEX:
        return data.cas22.replacements
    elif template == CAS_230000_TEX:
        return data.cas23.replacements
    elif template == CAS_240000_TEX:
        return data.cas24.replacements
    elif template == CAS_250000_TEX:
        return data.cas25.replacements
    elif template == CAS_260000_TEX:
        return data.cas26.replacements
    elif template == CAS_270000_TEX:
        return data.cas27.replacements
    elif template == CAS_280000_TEX:
        return data.cas28.replacements
    elif template == CAS_290000_TEX:
        return data.cas29.replacements
    elif template == CAS_300000_TEX:
        return data.cas30.replacements
    elif template == CAS_400000_TEX:
        return data.cas40.replacements
    elif template == CAS_500000_TEX:
        return data.cas50.replacements
    elif template == CAS_600000_TEX:
        return data.cas60.replacements
    elif template == CAS_700000_TEX:
        return data.cas70.replacements
    elif template == CAS_800000_DT_TEX:
        return compute_cas_800000_replacements(inputs.blanket, data.cas80)
    elif template == CAS_900000_TEX:
        return {'C900000': str(data.cas90.C900000)}
    elif template == LCOE_TEX:
        return compute_lcoe_replacements(inputs, data)
    elif template == CAS_STRUCTURE_TEX:
        return data.cost_table.replacements
    else:
        raise ValueError(f'Unrecognized template {template}')


def replace_values(template_content: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        template_content = template_content.replace(key, str(value))
    return template_content
