from importlib import resources

from pyfecons import Materials
from pyfecons.helpers import currency_str
from pyfecons.inputs import Inputs, Coils, SupplementaryHeating, PrimaryStructure, VacuumSystem, Basic, Blanket, \
    FuelHandling, LsaLevels
from pyfecons.data import Data, CAS22, CAS30, CAS40
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

POWER_TABLE_MFE_DT_TEX = 'powerTableMFEDT.tex'
CAS_100000_TEX = 'CAS100000.tex'
CAS_200000_TEX = 'CAS200000.tex'
CAS_210000_TEX = 'CAS210000.tex'
CAS_220101_TEX = 'CAS220101.tex'  # referenced as CAS220101_MFE_DT.tex in Jupyter
CAS_220102_TEX = 'CAS220102.tex'
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

TEMPLATE_FILES = [
    POWER_TABLE_MFE_DT_TEX,
    CAS_100000_TEX,
    CAS_200000_TEX,
    CAS_210000_TEX,
    CAS_220101_TEX,
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
        'C220203': cas22.C220203, # not in template
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
        'C220000': cas22.C220000, # TODO - currently not in the template
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
        'FLIBE_RHO': materials.Flibe.rho,
        'FLIBE_C': materials.Flibe.c,
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
        'C300000XXX': str(cas30.C300000), # not in template
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
        'C400000XXX': str(cas40.C400000), # TODO - not in template
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
            '00ETAP': inputs.power_table.eta_p,  # Pumping power capture efficiency
            'PTH': data.power_table.p_th,  # Thermal Power
            'ETATH': inputs.power_table.eta_th,  # Thermal conversion efficiency
            'PET': data.power_table.p_et,  # Total (Gross) Electric Power
            # 2. Recirculating power
            'PLOSS': data.power_table.p_loss,  # Lost Power
            'PCOILS': data.power_table.p_coils,  # Power into coils
            '000PTF': inputs.power_table.p_tf,  # Power into TF coils
            '000PPF': inputs.power_table.p_pf,  # Power into PF (equilibrium) coils
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
            'RECFRAC': round(data.power_table.recfrac, 3),  # Recirculating power fraction
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
    elif template == CAS_200000_TEX:
        return {'C200000': str(data.cas20.C200000)} # TODO - C200000 not in the template
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
            'C220101': currency_str(data.cas22.C220101),  # TODO - verify this is correct in template
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
            'primaryC': inputs.blanket.primary_coolant.display_name,
            'secondaryC': inputs.blanket.secondary_coolant.display_name,
            'neutronM': inputs.blanket.neutron_multiplier.display_name,
            'structure1': inputs.blanket.structure.display_name,
            'firstW': inputs.blanket.first_wall.display_name,
        }
    elif template == CAS_220102_TEX:
        return {
            'C22010201': round(data.cas22.C22010201),
            'C22010202': round(data.cas22.C22010202),
            'C22010203': round(data.cas22.C22010203),
            'C22010204': round(data.cas22.C22010204),
            'C22010200': round(data.cas22.C220102),
            'V220102': round(data.cas22.V_HTS),  # Missing from CAS220102.tex
            'primaryC': inputs.blanket.primary_coolant.display_name,
            'VOL9': round(data.cas22.ht_shield_vol),
            'VOL11': round(data.cas22.lt_shield_vol),  # Missing from CAS220102.tex
        }
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
    else:
        raise ValueError(f'Unrecognized template {template}')


def replace_values(template_content: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        template_content = template_content.replace(key, str(value))
    return template_content
