from pyfecons.helpers import currency_str
from pyfecons.inputs import Inputs, Coils
from pyfecons.data import Data, CAS22
from pyfecons.costing.mfe.PowerBalance import GenerateData as PowerBalanceData
from pyfecons.costing.mfe.CAS10 import GenerateData as CAS10Data
from pyfecons.costing.mfe.CAS21 import GenerateData as CAS21Data
from pyfecons.costing.mfe.CAS22 import GenerateData as CAS22Data

import os

POWER_TABLE_MFE_DT_TEX = 'powerTableMFEDT.tex'
CAS_100000_TEX = 'CAS100000.tex'
CAS_210000_TEX = 'CAS210000.tex'
CAS_220101_TEX = 'CAS220101.tex'  # referenced as CAS220101_MFE_DT.tex in Jupyter
CAS_220102_TEX = 'CAS220102.tex'
CAS_220103_TEX = 'CAS220103.tex'

TEMPLATE_FILES = [
    POWER_TABLE_MFE_DT_TEX,
    CAS_100000_TEX,
    CAS_210000_TEX,
    CAS_220101_TEX,
    CAS_220102_TEX,
    CAS_220103_TEX,
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


def compute_cas_220103_replacements(coils: Coils, cas22: CAS22) -> dict[str, str]:
    return {
        'C22010300': str(cas22.C220103),
        'C22010301': str(cas22.C22010301),
        'C22010302': str(cas22.C22010302),
        'C22010303': str(cas22.C22010303),
        'C22010304': str(cas22.C22010304),
        # 'C22010305': str(cas22.C22010305), # TODO - this was reference in template, but I just used C22010304
        'TABLE_STRUCTURE': ('l' + 'c' * len(cas22.magnet_properties)),
        'TABLE_HEADER_LIST': (" & ".join([f"\\textbf{{{props.magnet.name}}}" for props in cas22.magnet_properties])),
        'MAGNET_RADIUS_LIST': (" & ".join([f"{props.magnet.r_centre}" for props in cas22.magnet_properties])),
        'MAGNET_DR_LIST': (" & ".join([f"{props.magnet.dr}" for props in cas22.magnet_properties])),
        'MAGNET_DZ_LIST': (" & ".join([f"{props.magnet.dz}" for props in cas22.magnet_properties])),
        'CURRENT_SUPPLY_LIST': (" & ".join([f"{props.current_supply}" for props in cas22.magnet_properties])),
        'CABLE_CURRENT_DENSITY_LIST': (" & ".join([f"{props.magnet.j_cable}" for props in cas22.magnet_properties])),
        'CONDUCTOR_CURRENT_DENSITY_LIST': (" & ".join([f"{coils.j_tape}" for _ in cas22.magnet_properties])),
        'CABLE_WIDTH_LIST': (" & ".join([f"{coils.cable_w}" for _ in cas22.magnet_properties])),
        'CABLE_HEIGHT_LIST': (" & ".join([f"{coils.cable_h}" for _ in cas22.magnet_properties])),
        'TOTAL_VOLUME_LIST': (" & ".join([f"{props.vol_coil}" for props in cas22.magnet_properties])),
        'CROSS_SECTIONAL_AREA_LIST': (" & ".join([f"{props.cs_area}" for props in cas22.magnet_properties])),
        'CABLE_TURNS_LIST': (" & ".join([f"{props.turns_c}" for props in cas22.magnet_properties])),
        'TOTAL_TURNS_OF_CONDUCTOR_LIST': (" & ".join([f"{props.turns_sc_tot}" for props in cas22.magnet_properties])),
        'LENGTH_OF_CONDUCTOR_LIST': (" & ".join([f"{props.tape_length}" for props in cas22.magnet_properties])),
        'CURRENT_PER_CONDUCTOR_LIST': (" & ".join([f"{props.tape_current}" for props in cas22.magnet_properties])),
        'COST_OF_SC_LIST': (" & ".join([f"{props.cost_sc}" for props in cas22.magnet_properties])),
        'COST_OF_COPPER_LIST': (" & ".join([f"{props.cost_cu}" for props in cas22.magnet_properties])),
        'COST_OF_SS_LIST': (" & ".join([f"{props.cost_ss}" for props in cas22.magnet_properties])),
        'TOTAL_MATERIAL_COST_LIST': (" & ".join([f"{props.tot_mat_cost}" for props in cas22.magnet_properties])),
        'MANUFACTURING_FACTOR_LIST': (" & ".join([f"{coils.mfr_factor}" for _ in cas22.magnet_properties])),
        'STRUCTURAL_COST_LIST': (" & ".join([f"{props.magnet_struct_cost}" for props in cas22.magnet_properties])),
        'QUANTITY_LIST': (" & ".join([f"{props.magnet.coil_count}" for props in cas22.magnet_properties])),
        'MAGNET_COST_LIST': (" & ".join([f"{props.magnet_cost}" for props in cas22.magnet_properties])),
        'MAGNET_TOTAL_COST_INDIVIDUAL_LIST': (
            " & ".join([f"{props.magnet_total_cost_individual}" for props in cas22.magnet_properties])),
        'MAGNET_TOTAL_COST_LIST': (
            " & ".join([f"{props.magnet_total_cost_individual}" for props in cas22.magnet_properties])),
    }


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
    elif template == CAS_220101_TEX:
        return {
            'C220101': currency_str(data.cas22.C220101), # TODO - verify this is correct in template
            'RAD12I': round(data.cas22.coil_ir),
            'RAD13I': round(data.cas22.bioshield_ir),
            'RAD10I': round(data.cas22.gap2_or, 1),
            'RAD11I': round(data.cas22.lt_shield_or, 1),
            'RAD1I': round(data.cas22.plasma_or, 1),
            'RAD2I': round(data.cas22.vacuum_or, 1),
            'RAD3I': round(data.cas22.firstwall_or, 1),
            'RAD4I': round(data.cas22.blanket1_or, 1),
            'RAD5I': round(data.cas22.structure_or, 1),
            'RAD6I': round(data.cas22.reflector_or, 1),
            'RAD7I': round(data.cas22.gap1_or, 1),
            'RAD8I': round(data.cas22.vessel_or, 1),
            'RAD9I': round(data.cas22.ht_shield_or, 1),
            'RAD12O': round(data.cas22.coil_or),
            'RAD13O': round(data.cas22.bioshield_or),
            'RAD10O': round(data.cas22.gap2_or, 1),
            'RAD11O': round(data.cas22.lt_shield_or, 1),
            'RAD1O': round(data.cas22.plasma_or, 1),
            'RAD2O': round(data.cas22.vacuum_or, 1),
            'RAD3O': round(data.cas22.firstwall_or, 1),
            'RAD4O': round(data.cas22.blanket1_or, 1),
            'RAD5O': round(data.cas22.structure_or, 1),
            'RAD6O': round(data.cas22.reflector_or, 1),
            'RAD7O': round(data.cas22.gap1_or, 1),
            'RAD8O': round(data.cas22.vessel_or, 1),
            'RAD9O': round(data.cas22.ht_shield_or, 1),
            'TH10': round(data.cas22.gap2_vol),
            'TH11': round(inputs.radial_build.lt_shield_t),
            'TH12': round(inputs.radial_build.coil_t),
            'TH13': round(inputs.radial_build.bioshield_t),
            'TH01': round(inputs.radial_build.plasma_t, 1),
            'TH02': round(inputs.radial_build.vacuum_t, 1),
            'TH03': round(inputs.radial_build.firstwall_t, 1),
            'TH04': round(inputs.radial_build.blanket1_t, 1),
            'TH05': round(inputs.radial_build.structure_t, 1),
            'TH06': round(inputs.radial_build.reflector_t, 1),
            'TH07': round(inputs.radial_build.gap1_t, 1),
            'TH08': round(inputs.radial_build.vessel_t, 1),
            'TH09': round(inputs.radial_build.ht_shield_t, 1),
            'VOL10': round(data.cas22.gap2_vol),
            'VOL11': round(data.cas22.lt_shield_vol),
            'VOL12': round(data.cas22.coil_vol),
            'VOL13': round(data.cas22.bioshield_vol),
            'VOL01': round(data.cas22.plasma_vol),
            'VOL02': round(data.cas22.vacuum_vol),
            'VOL03': round(data.cas22.firstwall_vol),
            'VOL04': round(data.cas22.blanket1_vol),
            'VOL05': round(data.cas22.structure_vol),
            'VOL06': round(data.cas22.reflector_vol),
            'VOL07': round(data.cas22.gap1_vol),
            'VOL08': round(data.cas22.vessel_vol),
            'VOL09': round(data.cas22.ht_shield_vol),
            'primaryC': inputs.blanket.primary_coolant.value,
            'secondaryC': inputs.blanket.secondary_coolant.value,
            'neutronM': inputs.blanket.neutron_multiplier.value,
            'structure1': inputs.blanket.structure.value,
            'firstW': inputs.blanket.first_wall.value,
        }
    elif template == CAS_220102_TEX:
        return {
            'C22010201': round(data.cas22.C22010201),
            'C22010202': round(data.cas22.C22010202),
            'C22010203': round(data.cas22.C22010203),
            'C22010204': round(data.cas22.C22010204),
            'C22010200': round(data.cas22.C220102),
            'V220102': round(data.cas22.V_HTS),  # Missing from CAS220102.tex
            'primaryC': inputs.blanket.primary_coolant.value,
            'VOL9': round(data.cas22.ht_shield_vol),
            'VOL11': round(data.cas22.lt_shield_vol),  # Missing from CAS220102.tex
        }
    elif template == CAS_220103_TEX:
        return compute_cas_220103_replacements(inputs.coils, data.cas22)
    else:
        raise ValueError(f'Unrecognized template {template}')


def replace_values(template_content: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        template_content = template_content.replace(key, str(value))
    return template_content
