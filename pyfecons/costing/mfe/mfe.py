from pyfecons.helpers import currency_str
from pyfecons.inputs import Inputs
from pyfecons.data import Data
from pyfecons.costing.mfe.PowerBalance import GenerateData as PowerBalanceData
from pyfecons.costing.mfe.CAS10 import GenerateData as CAS10Data
from pyfecons.costing.mfe.CAS21 import GenerateData as CAS21Data
from pyfecons.costing.mfe.CAS22 import GenerateData as CAS22Data

import os

POWER_TABLE_MFE_DT_TEX = 'powerTableMFEDT.tex'
CAS_100000_TEX = 'CAS100000.tex'
CAS_210000_TEX = 'CAS210000.tex'

TEMPLATE_FILES = [
    POWER_TABLE_MFE_DT_TEX,
    CAS_100000_TEX,
    CAS_210000_TEX,
]


def GenerateData(inputs: Inputs) -> Data:
    data = Data()
    figures = {}
    PowerBalanceData(inputs, data, figures)
    CAS10Data(inputs, data, figures)
    CAS21Data(inputs, data, figures)
    CAS22Data(inputs, data, figures)
    return data


def HydrateTemplates(inputs: Inputs, data: Data) -> dict[str, str]:
    hydrated_templates = {}
    for template in TEMPLATE_FILES:
        template_content = read_template(template)
        replacements = get_template_replacements(template, inputs, data)
        hydrated_templates[template] = replace_values(template_content, replacements)
    return hydrated_templates


def read_template(template_file: str) -> str:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, 'templates', template_file)
    with open(template_path, 'r') as file:
        template_content = file.read()
    return template_content


def get_template_replacements(template: str, inputs: Inputs, data: Data) -> dict[str, str]:
    if template == POWER_TABLE_MFE_DT_TEX:
        return {
            # Ordered by occurrence in template
            # 1. Output power
            'PNRL': inputs.basic.p_nrl,  # Fusion Power
            'PALPHA': data.power_table.p_alpha,  # Alpha Power
            'PNEUTRON': data.power_table.p_neutron,  # Neutron Power
            'MN': inputs.power_table.mn,  # Neutron Energy Multiplier
            'ETAP': inputs.power_table.eta_p,  # Pumping power capture efficiency
            'PTH': data.power_table.p_th,  # Thermal Power
            'ETATH': inputs.power_table.eta_th,  # Thermal conversion efficiency
            'PET': data.power_table.p_et,  # Total (Gross) Electric Power
            # 2. Recirculating power
            'PLOSS': data.power_table.p_loss,  # Lost Power
            'PCOILS': data.power_table.p_coils,  # Power into coils
            'PTF': inputs.power_table.p_tf,  # Power into TF coils
            'PPF': inputs.power_table.p_pf,  # Power into PF (equilibrium) coils
            'FPCPPF': inputs.power_table.fpcppf,  # Primary Coolant Pumping Power Fraction
            'PPUMP': data.power_table.p_pump,  # Primary Coolant Pumping Power
            'FSUB': inputs.power_table.f_sub,  # Subsystem and Control Fraction
            'PSUB': data.power_table.p_sub,  # Subsystem and Control Power
            'PAUX': data.power_table.p_aux,  # Auxiliary systems
            'PTRIT': inputs.power_table.p_trit,  # Tritium Systems
            'PHOUSE': inputs.power_table.p_house,  # Housekeeping power
            'PCOOL': data.power_table.p_cool,  # Cooling systems
            'PTFCOOL': inputs.power_table.p_tfcool,  # TF coil cooling
            'PPFCOOL': inputs.power_table.p_pfcool,  # PF coil cooling
            'PCRYO': inputs.power_table.p_cryo,  # Cryo vacuum pumping
            'ETAPIN': inputs.power_table.eta_pin,  # Input power wall plug efficiency
            'PINPUT': inputs.power_table.p_input,  # Input power
            # 3. Outputs
            'QSCI': data.power_table.qsci,  # Scientific Q
            'QENG': data.power_table.qeng,  # Engineering Q
            'RECFRAC': data.power_table.recfrac,  # Recirculating power fraction
            'PNET': data.power_table.p_net,  # Output Power (Net Electric Power)
            # Included in powerTableMFEDTM.tex but missing in powerTableMFEDT.tex
            # 'PTHE': PTHE,
            # 'ETADE': ETADE,
            # 'PDEE': PDEE,
        }
    elif template == CAS_100000_TEX:
        return {
            'Nmod': str(inputs.basic.n_mod),
            'C100000': currency_str(data.cas10.C100000),
            'C110000': currency_str(data.cas10.C110000),
            'C120000': currency_str(data.cas10.C120000),
            'C130000': currency_str(data.cas10.C130000),
            'C140000': currency_str(data.cas10.C140000),
            'C150000': currency_str(data.cas10.C150000),
            'C160000': currency_str(data.cas10.C160000),
            'C170000': currency_str(data.cas10.C170000),
            'C190000': currency_str(data.cas10.C190000),
        }
    elif template == CAS_210000_TEX:
        return {
            'C210000': currency_str(data.cas21.C210000),
            'C210100': currency_str(data.cas21.C210100),
            'C210200': currency_str(data.cas21.C210200),
            'C210300': currency_str(data.cas21.C210300),
            'C210400': currency_str(data.cas21.C210400),
            'C210500': currency_str(data.cas21.C210500),
            'C210600': currency_str(data.cas21.C210600),
            'C210700': currency_str(data.cas21.C210700),
            'C210800': currency_str(data.cas21.C210800),
            'C210900': currency_str(data.cas21.C210900),
            'C211000': currency_str(data.cas21.C211000),
            'C211100': currency_str(data.cas21.C211100),
            'C211200': currency_str(data.cas21.C211200),
            'C211300': currency_str(data.cas21.C211300),
            'C211400': currency_str(data.cas21.C211400),
            'C211500': currency_str(data.cas21.C211500),
            'C211600': currency_str(data.cas21.C211600),
            'C211700': currency_str(data.cas21.C211700),
            # not in template file or data
            # 'C211900': currency_str(data.cas21.C211900),
        }
    else:
        raise ValueError(f'Unrecognized template {template}')


def replace_values(template_content: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        template_content = template_content.replace(key, str(value))
    return template_content
