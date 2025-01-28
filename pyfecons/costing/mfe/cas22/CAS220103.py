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
from pyfecons.data import (
    Data,
    TemplateProvider,
    MagnetProperties,
    CAS220103Coils,
    PowerTable,
)
from pyfecons.enums import MagnetMaterialType, MagnetType
from pyfecons.inputs import Inputs, Coils, Magnet, RadialBuild
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


def cas_220103_coils(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.3: Coils
    IN = inputs.coils
    OUT: CAS220103Coils = data.cas220103
    assert isinstance(OUT, CAS220103Coils)

    OUT.magnet_properties = [
        compute_magnet_properties(IN, magnet, inputs, data) for magnet in IN.magnets
    ]

    # Assign calculated totals to variables for .tex file
    OUT.C22010301 = M_USD(sum([mag.magnet_total_cost for mag in OUT.tf_coils]))
    OUT.C22010302 = M_USD(sum([mag.magnet_total_cost for mag in OUT.cs_coils]))
    OUT.C22010303 = M_USD(sum([mag.magnet_total_cost for mag in OUT.pf_coils]))
    # Shim coil costs, taken as 5% total primary magnet costs
    OUT.C22010304 = 0.05 * (OUT.C22010301 + OUT.C22010302 + OUT.C22010303)
    OUT.C22010305 = M_USD(
        sum([mag.magnet_struct_cost for mag in OUT.magnet_properties])
    )  # Structural cost
    OUT.C22010306 = M_USD(
        sum([mag.cooling_cost for mag in OUT.magnet_properties])
    )  # cooling cost
    # Total cost
    OUT.C220103 = M_USD(
        OUT.C22010301
        + OUT.C22010302
        + OUT.C22010303
        + OUT.C22010304
        + OUT.C22010305
        + OUT.C22010306
    )

    # Additional totals and calculations
    OUT.no_pf_coils = Count(sum(magnet.magnet.coil_count for magnet in OUT.pf_coils))
    OUT.no_pf_pairs = Count(OUT.no_pf_coils / 2)

    OUT.template_file = "CAS220103_MFE_DT_tokamak.tex"
    OUT.replacements = {
        "C220103__": str(OUT.C220103),
        "C22010301": str(OUT.C22010301),
        "C22010302": str(OUT.C22010302),
        "C22010303": str(OUT.C22010303),
        "C22010304": str(OUT.C22010304),
        "C22010305": str(OUT.C22010305),  # TODO not in template, should it be?
        "C22010306": str(OUT.C22010306),  # TODO not in template, should it be?
        "structFactor": IN.struct_factor,  # TODO not in template, should it be?
        "mcostI": IN.m_cost_ybco,  # TODO why is identical to mCostYBCO, not in template, should it be?
        "nopfcoils": OUT.no_pf_coils,  # TODO not in template, should it be?
        "nopfpairs": OUT.no_pf_pairs,  # TODO not in template, should it be?
        "mCostYBCO": IN.m_cost_ybco,  # TODO not in template, should it be?
        "tableStructure": ("l" + "c" * len(OUT.magnet_properties)),
        "tableHeaderList": (
            " & ".join(
                [f"\\textbf{{{props.magnet.name}}}" for props in OUT.magnet_properties]
            )
        ),
        "magnetTypeList": (
            " & ".join(
                [
                    f"\\textbf{{{props.magnet.material_type.display_name}}}"
                    for props in OUT.magnet_properties
                ]
            )
        ),
        "magnetRadiusList": (
            " & ".join([f"{props.magnet.r_centre}" for props in OUT.magnet_properties])
        ),
        "magnetDrList": (
            " & ".join([f"{props.magnet.dr}" for props in OUT.magnet_properties])
        ),
        "magnetDzList": (
            " & ".join([f"{props.magnet.dz}" for props in OUT.magnet_properties])
        ),
        "currentSupplyList": (
            " & ".join([f"{props.current_supply}" for props in OUT.magnet_properties])
        ),
        "conductorCurrentDensityList": (
            " & ".join([f"{props.j_tape}" for props in OUT.magnet_properties])
        ),
        "cableWidthList": (
            " & ".join([f"{props.cable_w}" for props in OUT.magnet_properties])
        ),
        "cableHeightList": (
            " & ".join([f"{props.cable_h}" for props in OUT.magnet_properties])
        ),
        "totalVolumeList": (
            " & ".join([f"{props.vol_coil}" for props in OUT.magnet_properties])
        ),
        "crossSectionalAreaList": (
            " & ".join([f"{props.cs_area}" for props in OUT.magnet_properties])
        ),
        "turnInsulationFractionList": (
            " & ".join([f"{props.magnet.frac_in}" for props in OUT.magnet_properties])
        ),
        "cableTurnsList": (
            " & ".join([f"{props.turns_c}" for props in OUT.magnet_properties])
        ),
        "totalTurnsOfConductorList": (
            " & ".join([f"{props.turns_scs}" for props in OUT.magnet_properties])
        ),
        "lengthOfConductorList": (
            " & ".join([f"{props.tape_length}" for props in OUT.magnet_properties])
        ),
        "currentPerConductorList": (
            " & ".join([f"{props.max_tape_current}" for props in OUT.magnet_properties])
        ),
        "costOfRebcoTapeList": (
            " & ".join([f"{IN.m_cost_ybco}" for _ in OUT.magnet_properties])
        ),
        "costOfScList": (
            " & ".join([f"{props.cost_sc}" for props in OUT.magnet_properties])
        ),
        "costOfCopperList": (
            " & ".join([f"{props.cost_cu}" for props in OUT.magnet_properties])
        ),
        "costOfStainlessSteelList": (
            " & ".join([f"{props.cost_ss}" for props in OUT.magnet_properties])
        ),
        "costOfTurnInsulationList": (
            " & ".join([f"{props.cost_i}" for props in OUT.magnet_properties])
        ),
        "totalMaterialCostList": (
            " & ".join([f"{props.tot_mat_cost}" for props in OUT.magnet_properties])
        ),
        "manufacturingFactorList": (
            " & ".join([f"{IN.mfr_factor}" for _ in OUT.magnet_properties])
        ),
        "structuralCostList": (
            " & ".join(
                [f"{props.magnet_struct_cost}" for props in OUT.magnet_properties]
            )
        ),
        "numberCoilsList": (
            " & ".join(
                [f"{props.magnet.coil_count}" for props in OUT.magnet_properties]
            )
        ),
        "magnetCostList": (
            " & ".join([f"{props.magnet_cost}" for props in OUT.magnet_properties])
        ),
        "magnetTotalCostIndividualList": (
            " & ".join(
                [
                    f"{props.magnet_total_cost_individual}"
                    for props in OUT.magnet_properties
                ]
            )
        ),
        "magnetTotalCostList": (
            " & ".join(
                [
                    f"{props.magnet_total_cost_individual}"
                    for props in OUT.magnet_properties
                ]
            )
        ),
    }
    return OUT


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
    coils: Coils, magnet: Magnet, inputs: Inputs, data: Data
) -> MagnetProperties:
    OUT = MagnetProperties()
    OUT.magnet = magnet

    yuhu = YuhuHtsCiccExtrapolation(magnet, True)

    OUT.turns_sc_tot = Turns(yuhu.r_turns * yuhu.z_turns)
    OUT.cable_w = coils.cable_w
    OUT.cable_h = coils.cable_h

    OUT.cs_area = Meters2(yuhu.dr * yuhu.dz)
    OUT.turns_c = Turns(OUT.cs_area / (coils.cable_w * coils.cable_h))
    OUT.turns_scs = Turns(OUT.turns_sc_tot / OUT.turns_c)
    OUT.current_supply = MA(OUT.turns_c * yuhu.cable_current)
    OUT.cable_current = Amperes(yuhu.cable_current)

    OUT.vol_coil = compute_magnet_volume(OUT, magnet, inputs.radial_build)
    OUT.tape_length = Kilometers(OUT.turns_sc_tot * magnet.r_centre * 2 * math.pi / 1e3)
    OUT.max_tape_current = Amperes(yuhu.cable_current / OUT.turns_scs)
    OUT.j_tape = coils.j_tape_ybco

    OUT.cost_sc = M_USD(
        OUT.max_tape_current / 1e3 * OUT.tape_length * 1e3 * coils.m_cost_ybco / 1e6
    )
    OUT.cost_cu = M_USD(
        coils.frac_cs_cu_yuhu * coils.m_cost_cu * OUT.vol_coil * coils.cu_density / 1e6
    )
    OUT.cost_ss = M_USD(
        coils.frac_cs_ss_yuhu * coils.m_cost_ss * OUT.vol_coil * coils.ss_density / 1e6
    )
    OUT.cost_i = M_USD(0)
    OUT.tot_mat_cost = M_USD(OUT.cost_sc + OUT.cost_cu + OUT.cost_ss)
    OUT.magnet_cost = M_USD(OUT.tot_mat_cost * coils.mfr_factor)
    OUT.coil_mass = Kilograms(
        (coils.rebco_density * OUT.tape_length * coils.tape_w * coils.tape_t)
        + (coils.frac_cs_cu_yuhu * OUT.vol_coil * coils.cu_density)
        + (coils.frac_cs_ss_yuhu * OUT.vol_coil * coils.ss_density)
    )
    OUT.cooling_cost = compute_magnet_cooling_cost(
        coils, magnet, OUT, data.power_table, inputs.radial_build
    )

    OUT.magnet_struct_cost = M_USD(
        coils.struct_factor * OUT.magnet_cost + OUT.cooling_cost
    )
    OUT.magnet_total_cost_individual = M_USD(OUT.magnet_cost + OUT.magnet_struct_cost)
    OUT.magnet_total_cost = M_USD(OUT.magnet_total_cost_individual * magnet.coil_count)

    return OUT


def compute_hts_cicc_magnet_properties(
    coils: Coils, magnet: Magnet, inputs: Inputs, data: Data
) -> MagnetProperties:
    OUT = MagnetProperties()
    OUT.magnet = magnet

    OUT.cable_w = coils.cable_w
    OUT.cable_h = coils.cable_h

    OUT.max_tape_current = coils.j_tape_ybco * coils.tape_w * 1e3 * coils.tape_t * 1e3
    OUT.turns_scs = Turns(
        (coils.cable_w * coils.cable_h * coils.frac_cs_sc_yuhu)
        / (coils.tape_w * coils.tape_t)
    )
    OUT.cable_current = Amperes(OUT.max_tape_current * OUT.turns_scs)

    OUT.cs_area = Meters2(magnet.dr * magnet.dz)
    OUT.turns_c = Turns(OUT.cs_area / (coils.cable_w * coils.cable_h))
    OUT.current_supply = MA(OUT.cable_current * OUT.turns_c)
    OUT.vol_coil = compute_magnet_volume(OUT, magnet, inputs.radial_build)

    OUT.turns_sc_tot = Turns(OUT.turns_scs * OUT.turns_c)
    OUT.tape_length = Kilometers(OUT.turns_sc_tot * magnet.r_centre * 2 * math.pi / 1e3)
    OUT.j_tape = coils.j_tape_ybco

    OUT.cost_sc = M_USD(
        OUT.max_tape_current / 1e3 * OUT.tape_length * 1e3 * coils.m_cost_ybco / 1e6
    )
    OUT.cost_cu = M_USD(
        coils.frac_cs_cu_yuhu * coils.m_cost_cu * OUT.vol_coil * coils.cu_density / 1e6
    )
    OUT.cost_ss = M_USD(
        coils.frac_cs_ss_yuhu * coils.m_cost_ss * OUT.vol_coil * coils.ss_density / 1e6
    )
    OUT.cost_i = M_USD(0)
    OUT.tot_mat_cost = M_USD(OUT.cost_sc + OUT.cost_cu + OUT.cost_ss)
    OUT.magnet_cost = M_USD(OUT.tot_mat_cost * coils.mfr_factor)
    OUT.coil_mass = Kilograms(
        (coils.rebco_density * OUT.tape_length * coils.tape_w * coils.tape_t)
        + (coils.frac_cs_cu_yuhu * OUT.vol_coil * coils.cu_density)
        + (coils.frac_cs_ss_yuhu * OUT.vol_coil * coils.ss_density)
    )
    OUT.cooling_cost = compute_magnet_cooling_cost(
        coils, magnet, OUT, data.power_table, inputs.radial_build
    )

    OUT.magnet_struct_cost = M_USD(
        coils.struct_factor * OUT.magnet_cost + OUT.cooling_cost
    )
    OUT.magnet_total_cost_individual = M_USD(OUT.magnet_cost + OUT.magnet_struct_cost)
    OUT.magnet_total_cost = M_USD(OUT.magnet_total_cost_individual * magnet.coil_count)

    return OUT


def compute_hts_pancake_magnet_properties(
    coils: Coils, magnet: Magnet, inputs: Inputs, data: Data
) -> MagnetProperties:
    OUT = MagnetProperties()
    OUT.magnet = magnet

    # Cables are not used here
    OUT.cable_w = Meters(0)
    OUT.cable_h = Meters(0)

    OUT.max_tape_current = Amperes(
        coils.j_tape_ybco * coils.tape_w * 1e3 * coils.tape_t * 1e3
    )
    OUT.cs_area = Meters2(magnet.dr * magnet.dz)
    OUT.turns_scs = Turns(
        (1 - magnet.frac_in) * OUT.cs_area / (coils.tape_w * coils.tape_t)
    )

    # in this case the 'cable' is the entire winding
    OUT.cable_current = Amperes(OUT.max_tape_current * OUT.turns_scs)
    OUT.vol_coil = compute_magnet_volume(OUT, magnet, inputs.radial_build)
    OUT.turns_c = Turns(0)
    OUT.turns_sc_tot = OUT.turns_scs
    OUT.current_supply = OUT.cable_current

    OUT.turns_i = Turns(magnet.frac_in * OUT.cs_area / (coils.tape_w * coils.tape_t))
    OUT.no_p = OUT.turns_scs / coils.turns_p

    # TODO are parenthesis correct here in the denominator?
    OUT.vol_i = Meters3(
        OUT.turns_scs
        * magnet.r_centre
        * 2
        * np.pi
        / 1e3
        * magnet.frac_in
        * (coils.tape_w * coils.tape_t)
    )
    OUT.tape_length = Kilometers(OUT.turns_sc_tot * magnet.r_centre * 2 * math.pi / 1e3)
    OUT.j_tape = coils.j_tape_ybco

    OUT.cost_sc = M_USD(
        OUT.max_tape_current / 1e3 * OUT.tape_length * 1e3 * coils.m_cost_ybco / 1e6
    )
    OUT.cost_i = to_m_usd(coils.m_cost_i * OUT.vol_i * coils.i_density / 1e6)
    OUT.cost_cu = M_USD(0)
    OUT.cost_ss = M_USD(0)
    OUT.tot_mat_cost = M_USD(OUT.cost_sc + OUT.cost_cu + OUT.cost_ss + OUT.cost_i)
    OUT.magnet_cost = M_USD(OUT.tot_mat_cost * magnet.mfr_factor)
    OUT.coil_mass = Kilograms(
        coils.rebco_density * OUT.tape_length * coils.tape_w * coils.tape_t
        + OUT.vol_i * coils.i_density
    )
    OUT.cooling_cost = compute_magnet_cooling_cost(
        coils, magnet, OUT, data.power_table, inputs.radial_build
    )

    OUT.magnet_struct_cost = M_USD(
        coils.struct_factor * OUT.magnet_cost + OUT.cooling_cost
    )
    OUT.magnet_total_cost_individual = M_USD(OUT.magnet_cost + OUT.magnet_struct_cost)
    OUT.magnet_total_cost = M_USD(OUT.magnet_total_cost_individual * magnet.coil_count)

    return OUT


def compute_copper_magnet_properties(
    coils: Coils, magnet: Magnet, inputs: Inputs, data: Data
) -> MagnetProperties:
    OUT = MagnetProperties()
    OUT.magnet = magnet

    OUT.cable_w = Meters(0)  # Cables are not used here
    OUT.cable_h = Meters(0)  # Cables are not used here

    # In this case 'Tape' refers to copper wire AWG 11
    OUT.cs_area = Meters2(magnet.dr * magnet.dz)

    OUT.turns_scs = Turns(
        (1 - magnet.frac_in) * OUT.cs_area / (0.5 * coils.cu_wire_d) ** 2
    )
    OUT.turns_i = Turns(magnet.frac_in * OUT.cs_area / (0.5 * coils.cu_wire_d) ** 2)

    OUT.vol_coil = compute_magnet_volume(OUT, magnet, inputs.radial_build)
    OUT.cu_wire_current = coils.max_cu_current
    OUT.max_tape_current = coils.max_cu_current
    OUT.j_tape = Amperes(coils.max_cu_current / (0.5 * coils.cu_wire_d * 1e3) ** 2)
    OUT.turns_sc_tot = OUT.turns_scs
    OUT.turns_c = Turns(0)
    OUT.cable_current = Amperes(0)
    OUT.tape_length = Kilometers(OUT.turns_scs * magnet.r_centre * 2 * np.pi / 1e3)
    OUT.current_supply = MA(OUT.cu_wire_current * OUT.turns_scs)

    OUT.vol_i = Meters3(magnet.frac_in * OUT.cs_area * magnet.r_centre * 2 * np.pi)
    OUT.cost_sc = M_USD(0)
    # simple volumetric material calc
    OUT.cost_cu = to_m_usd(
        (OUT.vol_coil - OUT.vol_i) * coils.cu_density * coils.m_cost_cu
    )
    OUT.cost_i = to_m_usd(coils.m_cost_i * OUT.vol_i * coils.i_density / 1e6)
    OUT.cost_ss = M_USD(0)
    OUT.tot_mat_cost = M_USD(OUT.cost_sc + OUT.cost_cu + OUT.cost_ss + OUT.cost_i)
    OUT.magnet_cost = M_USD(OUT.tot_mat_cost * magnet.mfr_factor)
    OUT.coil_mass = Kilograms(
        ((OUT.vol_coil - OUT.vol_i) * coils.cu_density) + (OUT.vol_i * coils.i_density)
    )
    OUT.cooling_cost = compute_magnet_cooling_cost(
        coils, magnet, OUT, data.power_table, inputs.radial_build
    )

    OUT.magnet_struct_cost = M_USD(
        coils.struct_factor * OUT.magnet_cost + OUT.cooling_cost
    )
    OUT.magnet_total_cost_individual = M_USD(OUT.magnet_cost + OUT.magnet_struct_cost)
    OUT.magnet_total_cost = M_USD(OUT.magnet_total_cost_individual * magnet.coil_count)

    return OUT


def compute_magnet_properties(
    coils: Coils, magnet: Magnet, inputs: Inputs, data: Data
) -> MagnetProperties:
    if magnet.material_type == MagnetMaterialType.HTS_CICC:
        if magnet.auto_cicc:
            return compute_hts_cicc_auto_magnet_properties(coils, magnet, inputs, data)
        else:
            return compute_hts_cicc_magnet_properties(coils, magnet, inputs, data)
    elif magnet.material_type == MagnetMaterialType.HTS_PANCAKE:
        return compute_hts_pancake_magnet_properties(coils, magnet, inputs, data)
    elif magnet.material_type == MagnetMaterialType.COPPER:
        return compute_copper_magnet_properties(coils, magnet, inputs, data)
    raise f"Unrecognized magnet material type {magnet.material_type}"


def compute_magnet_volume(
    properties: MagnetProperties, magnet: Magnet, radial_build: RadialBuild
) -> Meters3:
    volume = properties.cs_area * 2 * np.pi * magnet.r_centre
    if magnet.type == MagnetType.TF:
        return Meters3(volume * radial_build.elon)
    else:
        return Meters3(volume)
