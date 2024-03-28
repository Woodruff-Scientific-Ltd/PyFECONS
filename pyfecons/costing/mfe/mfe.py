from importlib import resources

from pyfecons import Materials
from pyfecons.inputs import Inputs, Coils, SupplementaryHeating, PrimaryStructure, VacuumSystem, Basic, Blanket, \
    FuelHandling, LsaLevels
from pyfecons.data import Data, CAS22, CAS30, CAS40, CAS50, CAS60, CAS80
from pyfecons.costing.mfe.PowerBalance import GenerateData as PowerBalanceData, POWER_TABLE_MFE_DT_TEX
from pyfecons.costing.mfe.CAS10 import GenerateData as CAS10Data, CAS_100000_TEX
from pyfecons.costing.mfe.CAS21 import GenerateData as CAS21Data, CAS_210000_TEX
from pyfecons.costing.mfe.CAS22 import GenerateData as CAS22Data, CAS_220101_MFE_DT_TEX, CAS_220102_TEX
from pyfecons.costing.mfe.CAS23 import GenerateData as CAS23Data
from pyfecons.costing.mfe.CAS24 import GenerateData as CAS24Data
from pyfecons.costing.mfe.CAS25 import GenerateData as CAS25Data
from pyfecons.costing.mfe.CAS26 import GenerateData as CAS26Data
from pyfecons.costing.mfe.CAS27 import GenerateData as CAS27Data
from pyfecons.costing.mfe.CAS28 import GenerateData as CAS28Data
from pyfecons.costing.mfe.CAS29 import GenerateData as CAS29Data
from pyfecons.costing.mfe.CAS20 import GenerateData as CAS20Data, CAS_200000_TEX
from pyfecons.costing.mfe.CAS30 import GenerateData as CAS30Data
from pyfecons.costing.mfe.CAS40 import GenerateData as CAS40Data
from pyfecons.costing.mfe.CAS50 import GenerateData as CAS50Data
from pyfecons.costing.mfe.CAS60 import GenerateData as CAS60Data
from pyfecons.costing.mfe.CAS70 import GenerateData as CAS70Data
from pyfecons.costing.mfe.CAS80 import GenerateData as CAS80Data
from pyfecons.costing.mfe.CAS90 import GenerateData as CAS90Data
from pyfecons.costing.mfe.LCOE import GenerateData as LCOEData
from pyfecons.costing.mfe.CostTable import GenerateData as CostTableData, CAS_STRUCTURE_TEX


CAS_220103_TEX = 'CAS220103.tex'
CAS_220104_TEX = 'CAS220104.tex'
CAS_220105_TEX = 'CAS220105.tex'
CAS_220106_TEX = 'CAS220106.tex'
CAS_220107_TEX = 'CAS220107.tex'
CAS_220108_TEX = 'CAS220108.tex'
CAS_220109_TEX = 'CAS220109.tex'
CAS_220111_TEX = 'CAS220111.tex'
CAS_220119_TEX = 'CAS220119.tex'
CAS_220200_TEX = 'CAS220200.tex'
CAS_220300_TEX = 'CAS220300.tex'
CAS_220400_TEX = 'CAS220400.tex'
CAS_220500_TEX = 'CAS220500.tex'
CAS_220600_TEX = 'CAS220600.tex'
CAS_220700_TEX = 'CAS220700.tex'
CAS_220000_TEX = 'CAS220000.tex'
CAS_230000_TEX = 'CAS230000.tex'
CAS_240000_TEX = 'CAS240000.tex'
CAS_250000_TEX = 'CAS250000.tex'
CAS_260000_TEX = 'CAS260000.tex'
CAS_270000_TEX = 'CAS270000.tex'
CAS_280000_TEX = 'CAS280000.tex'
CAS_290000_TEX = 'CAS290000.tex'
CAS_300000_TEX = 'CAS300000.tex'
CAS_400000_TEX = 'CAS400000.tex'
CAS_500000_TEX = 'CAS500000.tex'
CAS_600000_TEX = 'CAS600000.tex'
CAS_700000_TEX = 'CAS700000.tex'
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
    CAS_220103_TEX,
    CAS_220104_TEX,
    CAS_220105_TEX,
    CAS_220106_TEX,
    CAS_220107_TEX,
    CAS_220108_TEX,
    CAS_220109_TEX,
    CAS_220111_TEX,
    CAS_220119_TEX,
    CAS_220200_TEX,
    CAS_220300_TEX,
    CAS_220400_TEX,
    CAS_220500_TEX,
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


def compute_cas_220104_replacements(supplementary_heating: SupplementaryHeating, cas22: CAS22) -> dict[str, str]:
    heating_table_rows = "\n".join([
        f"        {ref.name} & {ref.type} & {ref.power} & {ref.cost_2023} & {ref.cost_2009} \\\\"
        for ref in supplementary_heating.heating_refs()
    ])
    return {
        'C22010401': str(round(cas22.C22010401, 3)),
        'C22010402': str(round(cas22.C22010402, 3)),
        'C22010400': str(round(cas22.C220104, 3)),
        'NBIpower': str(round(supplementary_heating.nbi_power, 3)),
        'ICRFpower': str(round(supplementary_heating.icrf_power, 3)),
        'HEATING_TABLE_ROWS': heating_table_rows,
    }


def compute_cas_220105_replacements(primary_structure: PrimaryStructure, cas22: CAS22) -> dict[str, str]:
    return {
        # TODO - next two fields are currently missing from the template
        'pgaengcosts': str(primary_structure.get_pga_costs().eng_costs),
        'pgafabcosts': str(primary_structure.get_pga_costs().fab_costs),
        'C22010501': str(cas22.C22010501),
        'C22010502': str(cas22.C22010502),
        'C22010500': str(cas22.C220105),
    }


def compute_cas_220106_replacements(vacuum_system: VacuumSystem, cas22: CAS22) -> dict[str, str]:
    return {
        'C22010601': round(cas22.C22010601),
        'C22010602': round(cas22.C22010601),
        'C22010603': round(cas22.C22010603),
        'C22010604': round(cas22.C22010604),
        'C22010600': round(cas22.C220106),
        'vesvol': round(cas22.vesvol),
        'materialvolume': round(cas22.materialvolume),
        'massstruct': round(cas22.massstruct),
        'vesmatcost': round(cas22.vesmatcost / 1e6, 1),
        'vesmfr': round(vacuum_system.vesmfr),
        'Qin': round(cas22.q_in, 2),
    }


def compute_cas_220107_replacements(basic: Basic, cas22: CAS22) -> dict[str, str]:
    return {
        'C220107': str(cas22.C220107),
        'PNRL': str(basic.p_nrl),
    }


def compute_cas_220108_replacements(cas22: CAS22) -> dict[str, str]:
    return {
        'C220108': round(cas22.C220108),
        'DIVERTOR_MAJ_RAD': cas22.divertor_maj_rad,
        'DIVERTOR_MIN_RAD': cas22.divertor_min_rad,
        'DIVERTOR_THICKNESS_Z': cas22.divertor_thickness_z,
        'DIVERTOR_MATERIAL_NAME': cas22.divertor_material.name,
        'DIVERTOR_VOL': cas22.divertor_vol,
        'DIVERTOR_MASS': cas22.divertor_mass,
    }


def compute_cas_220109_replacements(cas22: CAS22) -> dict[str, str]:
    replacements = {key: str(value) for key, value in cas22.scaled_direct_energy_costs.items()}
    replacements['C220109'] = cas22.C220109
    return replacements


def compute_cas_220200_replacements(blanket: Blanket, cas22: CAS22) -> dict[str, str]:
    return {
        'C220200': cas22.C220200,
        'C220201': cas22.C220201,
        'C220202': cas22.C220202,
        'C220203': cas22.C220203,  # not in template
        'primaryC': blanket.primary_coolant.display_name,
        'secondaryC': blanket.secondary_coolant.display_name,
    }


def compute_cas_220500_replacements(fuel_handling: FuelHandling, cas22: CAS22) -> dict[str, str]:
    return {
        'LEARNING_CURVE_CREDIT': fuel_handling.learning_curve_credit,
        'LEARNING_TENTH_OF_A_KIND': fuel_handling.learning_tenth_of_a_kind,
        'C2205010ITER': cas22.C2205010ITER,
        'C2205020ITER': cas22.C2205020ITER,
        'C2205030ITER': cas22.C2205030ITER,
        'C2205040ITER': cas22.C2205040ITER,
        'C2205050ITER': cas22.C2205050ITER,
        'C2205060ITER': cas22.C2205060ITER,
        'C22050ITER': cas22.C22050ITER,
        'C220501': cas22.C220501,
        'C220502': cas22.C220502,
        'C220503': cas22.C220503,
        'C220504': cas22.C220504,
        'C220505': cas22.C220505,
        'C220506': cas22.C220506,
        'C220500': cas22.C220500,
    }


def compute_cas_220000_replacements(materials: Materials, cas22: CAS22) -> dict[str, str]:
    return {
        'C220000': cas22.C220000,  # TODO - currently not in the template
        'BFS_RHO': materials.BFS.rho,
        'BFS_CRAW': materials.BFS.c_raw,
        'BFS_M': materials.BFS.m,
        'FS_RHO': materials.FS.rho,
        'FS_CRAW': materials.FS.c_raw,
        'FS_M': materials.FS.m,
        'FS_SIGMA': materials.FS.sigma,
        'LI4SIO4_RHO': materials.Li4SiO4.rho,
        'LI4SIO4_CRAW': materials.Li4SiO4.c_raw,
        'LI4SIO4_M': materials.Li4SiO4.m,
        'FLIBE_RHO': materials.FliBe.rho,
        'FLIBE_C': materials.FliBe.c,
        'W_RHO': materials.W.rho,
        'W_CRAW': materials.W.c_raw,
        'W_M': materials.W.m,
        'SIC_RHO': materials.SiC.rho,
        'SIC_CRAW': materials.SiC.c_raw,
        'SIC_M': materials.SiC.m,
        'INCONEL_RHO': materials.Inconel.rho,
        'INCONEL_CRAW': materials.Inconel.c_raw,
        'INCONEL_M': materials.Inconel.m,
        'CU_RHO': materials.Cu.rho,
        'CU_CRAW': materials.Cu.c_raw,
        'CU_M': materials.Cu.m,
        'POLYIMIDE_RHO': materials.Polyimide.rho,
        'POLYIMIDE_CRAW': materials.Polyimide.c_raw,
        'POLYIMIDE_M': materials.Polyimide.m,
        'YBCO_RHO': materials.YBCO.rho,
        'YBCO_C': materials.YBCO.c,
        'CONCRETE_RHO': materials.Concrete.rho,
        'CONCRETE_CRAW': materials.Concrete.c_raw,
        'CONCRETE_M': materials.Concrete.m,
        'SS316_RHO': materials.SS316.rho,
        'SS316_CRAW': materials.SS316.c_raw,
        'SS316_M': materials.SS316.m,
        'SS316_SIGMA': materials.SS316.sigma,
        'NB3SN_C': materials.Nb3Sn.c,
        'INCOLOY_RHO': materials.Incoloy.rho,
        'INCOLOY_CRAW': materials.Incoloy.c_raw,
        'INCOLOY_M': materials.Incoloy.m,
        'PB_RHO': materials.Pb.rho,
        'PB_CRAW': materials.Pb.c_raw,
        'PB_M': round(materials.Pb.m, 2),
        'PBLI_RHO': round(materials.PbLi.rho, 2),
        'PBLI_C': round(materials.PbLi.c, 2),
        'LI_RHO': materials.Li.rho,
        'LI_CRAW': materials.Li.c_raw,
        'LI_M': materials.Li.m,
    }


def compute_cas_300000_replacements(basic: Basic, cas30: CAS30) -> dict[str, str]:
    return {
        'constructionTime': str(basic.construction_time),
        'C300000XXX': str(cas30.C300000),  # TODO - not in template
        'C320000XXX': str(cas30.C320000),
        'C310000LSA': str(cas30.C310000LSA),
        'C310000XXX': str(cas30.C310000),
        'C350000LSA': str(cas30.C350000LSA),
        'C350000XXX': str(cas30.C350000),
    }


def compute_cas_400000_replacements(lsa_levels: LsaLevels, cas40: CAS40) -> dict[str, str]:
    return {
        'LSA_LEVEL': str(lsa_levels.lsa),
        'C400000LSA': str(cas40.C400000LSA),
        'C400000XXX': str(cas40.C400000),  # TODO - not in template
    }


def compute_cas_500000_replacements(cas50: CAS50) -> dict[str, str]:
    return {
        'C500000': str(cas50.C500000),  # TODO - not in template
        'C510000': str(cas50.C510000),
        'C520000': str(cas50.C520000),
        'C530000': str(cas50.C530000),
        'C540000': str(cas50.C540000),
        'C550000': str(cas50.C550000),
        'C580000': str(cas50.C580000),
        'C590000': str(cas50.C590000),
    }


def compute_cas_600000_replacements(cas60: CAS60) -> dict[str, str]:
    return {
        'C600000': str(cas60.C600000),  # TODO - not in template
        'C610000': str(cas60.C610000),
        'C630000LSA': str(cas60.C630000LSA),
        'C630000XXX': str(cas60.C630000),
    }


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
    elif template == CAS_220103_TEX:
        return compute_cas_220103_replacements(inputs.coils, data.cas22)
    elif template == CAS_220104_TEX:
        return compute_cas_220104_replacements(inputs.supplementary_heating, data.cas22)
    elif template == CAS_220105_TEX:
        return compute_cas_220105_replacements(inputs.primary_structure, data.cas22)
    elif template == CAS_220106_TEX:
        return compute_cas_220106_replacements(inputs.vacuum_system, data.cas22)
    elif template == CAS_220107_TEX:
        return compute_cas_220107_replacements(inputs.basic, data.cas22)
    elif template == CAS_220108_TEX:
        return compute_cas_220108_replacements(data.cas22)
    elif template == CAS_220109_TEX:
        return compute_cas_220109_replacements(data.cas22)
    elif template == CAS_220111_TEX:
        return {'C220111': str(data.cas22.C220111)}
    elif template == CAS_220119_TEX:
        return {'C220119': str(data.cas22.C220119)}
    elif template == CAS_220200_TEX:
        return compute_cas_220200_replacements(inputs.blanket, data.cas22)
    elif template == CAS_220300_TEX:
        return {'C220300': str(data.cas22.C220300)}
    elif template == CAS_220400_TEX:
        return {'C220400': str(data.cas22.C220400)}
    elif template == CAS_220500_TEX:
        return compute_cas_220500_replacements(inputs.fuel_handling, data.cas22)
    elif template == CAS_220600_TEX:
        return {'C220600': str(data.cas22.C220600)}
    elif template == CAS_220700_TEX:
        return {'C220700': str(data.cas22.C220700)}
    elif template == CAS_220000_TEX:
        return compute_cas_220000_replacements(inputs.materials, data.cas22)
    elif template == CAS_230000_TEX:
        return {'C230000': str(data.cas23.C230000)}
    elif template == CAS_240000_TEX:
        return {'C240000': str(data.cas24.C240000)}
    elif template == CAS_250000_TEX:
        return {'C250000': str(data.cas25.C250000)}
    elif template == CAS_260000_TEX:
        return {'C260000': str(data.cas26.C260000)}
    elif template == CAS_270000_TEX:
        return {'C270000': str(data.cas27.C270000)}
    elif template == CAS_280000_TEX:
        return {'C280000': str(data.cas28.C280000)}
    elif template == CAS_290000_TEX:
        return {'C290000': str(data.cas29.C290000)}
    elif template == CAS_300000_TEX:
        return compute_cas_300000_replacements(inputs.basic, data.cas30)
    elif template == CAS_400000_TEX:
        return compute_cas_400000_replacements(inputs.lsa_levels, data.cas40)
    elif template == CAS_500000_TEX:
        return compute_cas_500000_replacements(data.cas50)
    elif template == CAS_600000_TEX:
        return compute_cas_600000_replacements(data.cas60)
    elif template == CAS_700000_TEX:
        return {'C700000': str(data.cas70.C700000)}
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
