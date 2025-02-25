import math
import numpy as np

from pyfecons.costing.calculations.YuhuHtsCiccExtrapolation import (
    YuhuHtsCiccExtrapolation,
)
from pyfecons.costing.calculations.conversions import w_to_mw, to_m_usd
from pyfecons.costing.calculations.thermal import (
    k_steel,
    compute_q_in_struct,
    compute_q_in_n,
    compute_iter_cost_per_MW,
)
from pyfecons.costing.models.magnet_properties import MagnetProperties
from pyfecons.costing.categories.cas220103_coils import CAS220103Coils
from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.enums import MagnetMaterialType, MagnetType
from pyfecons.inputs.coils import Coils
from pyfecons.inputs.magnet import Magnet
from pyfecons.inputs.radial_build import RadialBuild
from pyfecons.units import (
    M_USD,
    Count,
    MW,
    Turns,
    Meters2,
    MA,
    Amperes,
    Meters3,
    Kilometers,
    Kilograms,
    Meters,
)


def cas_220103_coils(coils: Coils, radial_build: RadialBuild, power_table: PowerTable) -> CAS220103Coils:
    # Cost Category 22.1.3: Coils
    cas220103 = CAS220103Coils()

    cas220103.magnet_properties = [
        compute_magnet_properties(coils, magnet, radial_build, power_table) for magnet in coils.magnets
    ]

    # Assign calculated totals to variables for .tex file
    cas220103.C22010301 = M_USD(sum([mag.magnet_total_cost for mag in cas220103.tf_coils]))
    cas220103.C22010302 = M_USD(sum([mag.magnet_total_cost for mag in cas220103.cs_coils]))
    cas220103.C22010303 = M_USD(sum([mag.magnet_total_cost for mag in cas220103.pf_coils]))
    # Shim coil costs, taken as 5% total primary magnet costs
    cas220103.C22010304 = 0.05 * (cas220103.C22010301 + cas220103.C22010302 + cas220103.C22010303)
    cas220103.C22010305 = M_USD(
        sum([mag.magnet_struct_cost for mag in cas220103.magnet_properties])
    )  # Structural cost
    cas220103.C22010306 = M_USD(
        sum([mag.cooling_cost for mag in cas220103.magnet_properties])
    )  # cooling cost
    # Total cost
    cas220103.C220103 = M_USD(
        cas220103.C22010301
        + cas220103.C22010302
        + cas220103.C22010303
        + cas220103.C22010304
        + cas220103.C22010305
        + cas220103.C22010306
    )

    # Additional totals and calculations
    cas220103.no_pf_coils = Count(sum(magnet.magnet.coil_count for magnet in cas220103.pf_coils))
    cas220103.no_pf_pairs = Count(cas220103.no_pf_coils / 2)

    cas220103.template_file = "CAS220103_MFE_DT_tokamak.tex"
    cas220103.replacements = {
        "C220103__": str(cas220103.C220103),
        "C22010301": str(cas220103.C22010301),
        "C22010302": str(cas220103.C22010302),
        "C22010303": str(cas220103.C22010303),
        "C22010304": str(cas220103.C22010304),
        "C22010305": str(cas220103.C22010305),  # TODO not in template, should it be?
        "C22010306": str(cas220103.C22010306),  # TODO not in template, should it be?
        "structFactor": coils.struct_factor,  # TODO not in template, should it be?
        "mcostI": coils.m_cost_ybco,  # TODO why is identical to mCostYBCO, not in template, should it be?
        "nopfcoils": cas220103.no_pf_coils,  # TODO not in template, should it be?
        "nopfpairs": cas220103.no_pf_pairs,  # TODO not in template, should it be?
        "mCostYBCO": coils.m_cost_ybco,  # TODO not in template, should it be?
        "tableStructure": ("l" + "c" * len(cas220103.magnet_properties)),
        "tableHeaderList": (
            " & ".join(
                [f"\\textbf{{{props.magnet.name}}}" for props in cas220103.magnet_properties]
            )
        ),
        "magnetTypeList": (
            " & ".join(
                [
                    f"\\textbf{{{props.magnet.material_type.display_name}}}"
                    for props in cas220103.magnet_properties
                ]
            )
        ),
        "magnetRadiusList": (
            " & ".join([f"{props.magnet.r_centre}" for props in cas220103.magnet_properties])
        ),
        "magnetDrList": (
            " & ".join([f"{props.magnet.dr}" for props in cas220103.magnet_properties])
        ),
        "magnetDzList": (
            " & ".join([f"{props.magnet.dz}" for props in cas220103.magnet_properties])
        ),
        "currentSupplyList": (
            " & ".join([f"{props.current_supply}" for props in cas220103.magnet_properties])
        ),
        "conductorCurrentDensityList": (
            " & ".join([f"{props.j_tape}" for props in cas220103.magnet_properties])
        ),
        "cableWidthList": (
            " & ".join([f"{props.cable_w}" for props in cas220103.magnet_properties])
        ),
        "cableHeightList": (
            " & ".join([f"{props.cable_h}" for props in cas220103.magnet_properties])
        ),
        "totalVolumeList": (
            " & ".join([f"{props.vol_coil}" for props in cas220103.magnet_properties])
        ),
        "crossSectionalAreaList": (
            " & ".join([f"{props.cs_area}" for props in cas220103.magnet_properties])
        ),
        "turnInsulationFractionList": (
            " & ".join([f"{props.magnet.frac_in}" for props in cas220103.magnet_properties])
        ),
        "cableTurnsList": (
            " & ".join([f"{props.turns_c}" for props in cas220103.magnet_properties])
        ),
        "totalTurnsOfConductorList": (
            " & ".join([f"{props.turns_scs}" for props in cas220103.magnet_properties])
        ),
        "lengthOfConductorList": (
            " & ".join([f"{props.tape_length}" for props in cas220103.magnet_properties])
        ),
        "currentPerConductorList": (
            " & ".join([f"{props.max_tape_current}" for props in cas220103.magnet_properties])
        ),
        "costOfRebcoTapeList": (
            " & ".join([f"{coils.m_cost_ybco}" for _ in cas220103.magnet_properties])
        ),
        "costOfScList": (
            " & ".join([f"{props.cost_sc}" for props in cas220103.magnet_properties])
        ),
        "costOfCopperList": (
            " & ".join([f"{props.cost_cu}" for props in cas220103.magnet_properties])
        ),
        "costOfStainlessSteelList": (
            " & ".join([f"{props.cost_ss}" for props in cas220103.magnet_properties])
        ),
        "costOfTurnInsulationList": (
            " & ".join([f"{props.cost_i}" for props in cas220103.magnet_properties])
        ),
        "totalMaterialCostList": (
            " & ".join([f"{props.tot_mat_cost}" for props in cas220103.magnet_properties])
        ),
        "manufacturingFactorList": (
            " & ".join([f"{coils.mfr_factor}" for _ in cas220103.magnet_properties])
        ),
        "structuralCostList": (
            " & ".join(
                [f"{props.magnet_struct_cost}" for props in cas220103.magnet_properties]
            )
        ),
        "numberCoilsList": (
            " & ".join(
                [f"{props.magnet.coil_count}" for props in cas220103.magnet_properties]
            )
        ),
        "magnetCostList": (
            " & ".join([f"{props.magnet_cost}" for props in cas220103.magnet_properties])
        ),
        "magnetTotalCostIndividualList": (
            " & ".join(
                [
                    f"{props.magnet_total_cost_individual}"
                    for props in cas220103.magnet_properties
                ]
            )
        ),
        "magnetTotalCostList": (
            " & ".join(
                [
                    f"{props.magnet_total_cost_individual}"
                    for props in cas220103.magnet_properties
                ]
            )
        ),
    }
    return cas220103


def compute_q_ohmic(wire_length: float, cu_wire_current: float) -> MW:
    # Resistance of 3.2 Ohms/1000m see https://www.engineeringtoolbox.com/copper-wire-d_1429.html
    cures = wire_length * 3.2
    return w_to_mw(cu_wire_current**2 * cures)


def compute_magnet_cooling_cost(
    coils: Coils,
    magnet: Magnet,
    properties: MagnetProperties,
    power_table: PowerTable,
    radial_build: RadialBuild,
) -> M_USD:
    # Neutron heat loading
    q_in_n = compute_q_in_n(magnet, power_table, radial_build)
    # For 1 coil, assume 20 support beams, 5m length, 0.5m^2 cs area, target temp of 20K, env temp of 300 K
    q_in_struct = compute_q_in_struct(
        coils,
        k_steel((coils.t_env + magnet.coil_temp) / 2),
        (coils.t_env + magnet.coil_temp) / 2,
    )
    q_in = q_in_struct + q_in_n  # total input heat for one coil
    if magnet.material_type == MagnetMaterialType.COPPER:
        q_in = q_in + compute_q_ohmic(
            properties.tape_length, properties.cu_wire_current
        )
    return M_USD(q_in * compute_iter_cost_per_MW(coils))


def compute_hts_cicc_auto_magnet_properties(
    coils: Coils, magnet: Magnet, radial_build: RadialBuild, power_table: PowerTable
) -> MagnetProperties:
    props = MagnetProperties()
    props.magnet = magnet

    yuhu = YuhuHtsCiccExtrapolation(magnet, True)

    props.turns_sc_tot = Turns(yuhu.r_turns * yuhu.z_turns)
    props.cable_w = coils.cable_w
    props.cable_h = coils.cable_h

    props.cs_area = Meters2(yuhu.dr * yuhu.dz)
    props.turns_c = Turns(props.cs_area / (coils.cable_w * coils.cable_h))
    props.turns_scs = Turns(props.turns_sc_tot / props.turns_c)
    props.current_supply = MA(props.turns_c * yuhu.cable_current)
    props.cable_current = Amperes(yuhu.cable_current)

    props.vol_coil = compute_magnet_volume(props, magnet, radial_build)
    props.tape_length = Kilometers(props.turns_sc_tot * magnet.r_centre * 2 * math.pi / 1e3)
    props.max_tape_current = Amperes(yuhu.cable_current / props.turns_scs)
    props.j_tape = coils.j_tape_ybco

    props.cost_sc = M_USD(
        props.max_tape_current / 1e3 * props.tape_length * 1e3 * coils.m_cost_ybco / 1e6
    )
    props.cost_cu = M_USD(
        coils.frac_cs_cu_yuhu * coils.m_cost_cu * props.vol_coil * coils.cu_density / 1e6
    )
    props.cost_ss = M_USD(
        coils.frac_cs_ss_yuhu * coils.m_cost_ss * props.vol_coil * coils.ss_density / 1e6
    )
    props.cost_i = M_USD(0)
    props.tot_mat_cost = M_USD(props.cost_sc + props.cost_cu + props.cost_ss)
    props.magnet_cost = M_USD(props.tot_mat_cost * coils.mfr_factor)
    props.coil_mass = Kilograms(
        (coils.rebco_density * props.tape_length * coils.tape_w * coils.tape_t)
        + (coils.frac_cs_cu_yuhu * props.vol_coil * coils.cu_density)
        + (coils.frac_cs_ss_yuhu * props.vol_coil * coils.ss_density)
    )
    props.cooling_cost = compute_magnet_cooling_cost(
        coils, magnet, props, power_table, radial_build
    )

    props.magnet_struct_cost = M_USD(
        coils.struct_factor * props.magnet_cost + props.cooling_cost
    )
    props.magnet_total_cost_individual = M_USD(props.magnet_cost + props.magnet_struct_cost)
    props.magnet_total_cost = M_USD(props.magnet_total_cost_individual * magnet.coil_count)

    return props


def compute_hts_cicc_magnet_properties(
    coils: Coils, magnet: Magnet, radial_build: RadialBuild, power_table: PowerTable
) -> MagnetProperties:
    props = MagnetProperties()
    props.magnet = magnet

    props.cable_w = coils.cable_w
    props.cable_h = coils.cable_h

    props.max_tape_current = coils.j_tape_ybco * coils.tape_w * 1e3 * coils.tape_t * 1e3
    props.turns_scs = Turns(
        (coils.cable_w * coils.cable_h * coils.frac_cs_sc_yuhu)
        / (coils.tape_w * coils.tape_t)
    )
    props.cable_current = Amperes(props.max_tape_current * props.turns_scs)

    props.cs_area = Meters2(magnet.dr * magnet.dz)
    props.turns_c = Turns(props.cs_area / (coils.cable_w * coils.cable_h))
    props.current_supply = MA(props.cable_current * props.turns_c)
    props.vol_coil = compute_magnet_volume(props, magnet, radial_build)

    props.turns_sc_tot = Turns(props.turns_scs * props.turns_c)
    props.tape_length = Kilometers(props.turns_sc_tot * magnet.r_centre * 2 * math.pi / 1e3)
    props.j_tape = coils.j_tape_ybco

    props.cost_sc = M_USD(
        props.max_tape_current / 1e3 * props.tape_length * 1e3 * coils.m_cost_ybco / 1e6
    )
    props.cost_cu = M_USD(
        coils.frac_cs_cu_yuhu * coils.m_cost_cu * props.vol_coil * coils.cu_density / 1e6
    )
    props.cost_ss = M_USD(
        coils.frac_cs_ss_yuhu * coils.m_cost_ss * props.vol_coil * coils.ss_density / 1e6
    )
    props.cost_i = M_USD(0)
    props.tot_mat_cost = M_USD(props.cost_sc + props.cost_cu + props.cost_ss)
    props.magnet_cost = M_USD(props.tot_mat_cost * coils.mfr_factor)
    props.coil_mass = Kilograms(
        (coils.rebco_density * props.tape_length * coils.tape_w * coils.tape_t)
        + (coils.frac_cs_cu_yuhu * props.vol_coil * coils.cu_density)
        + (coils.frac_cs_ss_yuhu * props.vol_coil * coils.ss_density)
    )
    props.cooling_cost = compute_magnet_cooling_cost(
        coils, magnet, props, power_table, radial_build
    )

    props.magnet_struct_cost = M_USD(
        coils.struct_factor * props.magnet_cost + props.cooling_cost
    )
    props.magnet_total_cost_individual = M_USD(props.magnet_cost + props.magnet_struct_cost)
    props.magnet_total_cost = M_USD(props.magnet_total_cost_individual * magnet.coil_count)

    return props


def compute_hts_pancake_magnet_properties(
    coils: Coils, magnet: Magnet, radial_build: RadialBuild, power_table: PowerTable
) -> MagnetProperties:
    props = MagnetProperties()
    props.magnet = magnet

    # Cables are not used here
    props.cable_w = Meters(0)
    props.cable_h = Meters(0)

    props.max_tape_current = Amperes(
        coils.j_tape_ybco * coils.tape_w * 1e3 * coils.tape_t * 1e3
    )
    props.cs_area = Meters2(magnet.dr * magnet.dz)
    props.turns_scs = Turns(
        (1 - magnet.frac_in) * props.cs_area / (coils.tape_w * coils.tape_t)
    )

    # in this case the 'cable' is the entire winding
    props.cable_current = Amperes(props.max_tape_current * props.turns_scs)
    props.vol_coil = compute_magnet_volume(props, magnet, radial_build)
    props.turns_c = Turns(0)
    props.turns_sc_tot = props.turns_scs
    props.current_supply = props.cable_current

    props.turns_i = Turns(magnet.frac_in * props.cs_area / (coils.tape_w * coils.tape_t))
    props.no_p = props.turns_scs / coils.turns_p

    # TODO are parenthesis correct here in the denominator?
    props.vol_i = Meters3(
        props.turns_scs
        * magnet.r_centre
        * 2
        * np.pi
        / 1e3
        * magnet.frac_in
        * (coils.tape_w * coils.tape_t)
    )
    props.tape_length = Kilometers(props.turns_sc_tot * magnet.r_centre * 2 * math.pi / 1e3)
    props.j_tape = coils.j_tape_ybco

    props.cost_sc = M_USD(
        props.max_tape_current / 1e3 * props.tape_length * 1e3 * coils.m_cost_ybco / 1e6
    )
    props.cost_i = to_m_usd(coils.m_cost_i * props.vol_i * coils.i_density / 1e6)
    props.cost_cu = M_USD(0)
    props.cost_ss = M_USD(0)
    props.tot_mat_cost = M_USD(props.cost_sc + props.cost_cu + props.cost_ss + props.cost_i)
    props.magnet_cost = M_USD(props.tot_mat_cost * magnet.mfr_factor)
    props.coil_mass = Kilograms(
        coils.rebco_density * props.tape_length * coils.tape_w * coils.tape_t
        + props.vol_i * coils.i_density
    )
    props.cooling_cost = compute_magnet_cooling_cost(
        coils, magnet, props, power_table, radial_build
    )

    props.magnet_struct_cost = M_USD(
        coils.struct_factor * props.magnet_cost + props.cooling_cost
    )
    props.magnet_total_cost_individual = M_USD(props.magnet_cost + props.magnet_struct_cost)
    props.magnet_total_cost = M_USD(props.magnet_total_cost_individual * magnet.coil_count)

    return props


def compute_copper_magnet_properties(
    coils: Coils, magnet: Magnet, radial_build: RadialBuild, power_table: PowerTable
) -> MagnetProperties:
    props = MagnetProperties()
    props.magnet = magnet

    props.cable_w = Meters(0)  # Cables are not used here
    props.cable_h = Meters(0)  # Cables are not used here

    # In this case 'Tape' refers to copper wire AWG 11
    props.cs_area = Meters2(magnet.dr * magnet.dz)

    props.turns_scs = Turns(
        (1 - magnet.frac_in) * props.cs_area / (0.5 * coils.cu_wire_d) ** 2
    )
    props.turns_i = Turns(magnet.frac_in * props.cs_area / (0.5 * coils.cu_wire_d) ** 2)

    props.vol_coil = compute_magnet_volume(props, magnet, radial_build)
    props.cu_wire_current = coils.max_cu_current
    props.max_tape_current = coils.max_cu_current
    props.j_tape = Amperes(coils.max_cu_current / (0.5 * coils.cu_wire_d * 1e3) ** 2)
    props.turns_sc_tot = props.turns_scs
    props.turns_c = Turns(0)
    props.cable_current = Amperes(0)
    props.tape_length = Kilometers(props.turns_scs * magnet.r_centre * 2 * np.pi / 1e3)
    props.current_supply = MA(props.cu_wire_current * props.turns_scs)

    props.vol_i = Meters3(magnet.frac_in * props.cs_area * magnet.r_centre * 2 * np.pi)
    props.cost_sc = M_USD(0)
    # simple volumetric material calc
    props.cost_cu = to_m_usd(
        (props.vol_coil - props.vol_i) * coils.cu_density * coils.m_cost_cu
    )
    props.cost_i = to_m_usd(coils.m_cost_i * props.vol_i * coils.i_density / 1e6)
    props.cost_ss = M_USD(0)
    props.tot_mat_cost = M_USD(props.cost_sc + props.cost_cu + props.cost_ss + props.cost_i)
    props.magnet_cost = M_USD(props.tot_mat_cost * magnet.mfr_factor)
    props.coil_mass = Kilograms(
        ((props.vol_coil - props.vol_i) * coils.cu_density) + (props.vol_i * coils.i_density)
    )
    props.cooling_cost = compute_magnet_cooling_cost(
        coils, magnet, props, power_table, radial_build
    )

    props.magnet_struct_cost = M_USD(
        coils.struct_factor * props.magnet_cost + props.cooling_cost
    )
    props.magnet_total_cost_individual = M_USD(props.magnet_cost + props.magnet_struct_cost)
    props.magnet_total_cost = M_USD(props.magnet_total_cost_individual * magnet.coil_count)

    return props


def compute_magnet_properties(
    coils: Coils, magnet: Magnet, radial_build: RadialBuild, power_table: PowerTable
) -> MagnetProperties:
    if magnet.material_type == MagnetMaterialType.HTS_CICC:
        if magnet.auto_cicc:
            return compute_hts_cicc_auto_magnet_properties(coils, magnet, radial_build, power_table)
        else:
            return compute_hts_cicc_magnet_properties(coils, magnet, radial_build, power_table)
    elif magnet.material_type == MagnetMaterialType.HTS_PANCAKE:
        return compute_hts_pancake_magnet_properties(coils, magnet, radial_build, power_table)
    elif magnet.material_type == MagnetMaterialType.COPPER:
        return compute_copper_magnet_properties(coils, magnet, radial_build, power_table)
    raise f"Unrecognized magnet material type {magnet.material_type}"


def compute_magnet_volume(
    properties: MagnetProperties, magnet: Magnet, radial_build: RadialBuild
) -> Meters3:
    volume = properties.cs_area * 2 * np.pi * magnet.r_centre
    if magnet.type == MagnetType.TF:
        return Meters3(volume * radial_build.elon)
    else:
        return Meters3(volume)
