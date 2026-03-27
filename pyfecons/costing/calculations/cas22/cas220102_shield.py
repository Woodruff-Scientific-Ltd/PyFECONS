import logging

from pyfecons.costing.calculations.conversions import k_to_m_usd
from pyfecons.costing.calculations.volume import calc_volume_ring, calc_volume_sphere
from pyfecons.costing.categories.cas220101 import CAS220101
from pyfecons.costing.categories.cas220102 import CAS220102
from pyfecons.costing.safety.bioshield import (
    BIOSHIELD_MATERIAL_PROPERTIES,
    compute_required_thickness_meters,
)
from pyfecons.enums import FusionMachineType
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.blanket import Blanket
from pyfecons.inputs.radial_build import RadialBuild
from pyfecons.inputs.shield import Shield
from pyfecons.materials import Materials
from pyfecons.units import M_USD, Meters, Meters3

logger = logging.getLogger(__name__)

materials = Materials()


def cas_220102_shield_costs(
    basic: Basic,
    shield: Shield,
    blanket: Blanket,
    cas220101: CAS220101,
    radial_build: RadialBuild = None,
) -> CAS220102:
    # Cost Category 22.1.2: Shield
    fusion_machine_type = basic.fusion_machine_type
    cas220102 = CAS220102()

    # Retrieve the volume of HTS from the reactor_volumes dictionary
    cas220102.V_HTS = round(cas220101.ht_shield_vol, 1)

    # Calculate the cost for HTS
    C_HTS = round(
        cas220102.V_HTS
        * (
            materials.SiC.rho * materials.SiC.c_raw * materials.SiC.m * shield.f_SiC
            + materials.PbLi.rho * materials.PbLi.c * shield.FPCPPFbLi
            + materials.W.rho * materials.W.c_raw * materials.W.m * shield.f_W
            + materials.BFS.rho * materials.BFS.c_raw * materials.BFS.m * shield.f_BFS
        )
        / 1e6,
        1,
    )

    # Volume of HTShield that is BFS
    # TODO this is unused
    V_HTS_BFS = cas220102.V_HTS * shield.f_BFS

    # The cost C_22_1_2 is the same as C_HTS
    # TODO what's the *5 for?
    c_hts_scaling = 5.0 if fusion_machine_type == FusionMachineType.IFE else 1.0
    cas220102.C22010201 = M_USD(round(C_HTS * c_hts_scaling, 1))
    cas220102.C22010202 = k_to_m_usd(
        cas220101.lt_shield_vol * materials.SS316.c_raw * materials.SS316.m
    )

    # CAS 22.01.02.03: Bioshield
    _compute_bioshield_cost(
        cas220102, basic, shield, cas220101, radial_build, fusion_machine_type
    )

    cas220102.C22010204 = M_USD(cas220102.C22010203 * 0.1)
    cas220102.C220102 = M_USD(
        cas220102.C22010201
        + cas220102.C22010202
        + cas220102.C22010203
        + cas220102.C22010204
    )

    return cas220102


def _compute_bioshield_cost(
    cas220102: CAS220102,
    basic: Basic,
    shield: Shield,
    cas220101: CAS220101,
    radial_build: RadialBuild,
    fusion_machine_type: FusionMachineType,
):
    """Compute bioshield cost. Dose-based when safety is enabled and
    bioshield inputs are present, otherwise existing geometry-only calc."""

    use_dose_based = (
        basic.include_safety_hazards_costs
        and shield.bioshield_material is not None
        and shield.initial_dose_without_bioshield is not None
        and shield.regulatory_dose_limit is not None
        and radial_build is not None
    )

    if not use_dose_based:
        # Existing behavior: geometry-only with SS316
        cas220102.C22010203 = k_to_m_usd(
            cas220101.bioshield_vol * materials.SS316.c_raw * materials.SS316.m
        )
        return

    # Dose-based calculation
    material = shield.bioshield_material
    initial_dose = shield.initial_dose_without_bioshield
    regulatory_dose = shield.regulatory_dose_limit
    props = BIOSHIELD_MATERIAL_PROPERTIES[material]

    # Step 1: Compute DTF and required thickness
    dtf = regulatory_dose / initial_dose
    required_thickness = compute_required_thickness_meters(
        material, initial_dose, regulatory_dose
    )

    # Step 2: Never shrink below user-specified bioshield_t
    user_thickness = radial_build.bioshield_t if radial_build.bioshield_t else 0
    effective_thickness = max(required_thickness, user_thickness)

    if effective_thickness > user_thickness and user_thickness > 0:
        logger.warning(
            "Bioshield dose calculation requires %.3f m thickness, "
            "but user specified %.3f m. Using dose-required thickness.",
            effective_thickness,
            user_thickness,
        )

    # Step 3: Recompute bioshield volume with effective thickness
    bioshield_ir = cas220101.bioshield_ir
    if fusion_machine_type == FusionMachineType.IFE:
        bioshield_vol = calc_volume_sphere(
            bioshield_ir, bioshield_ir + effective_thickness
        )
    else:
        # MFE: use axis_t (tokamak) or chamber_length (mirror) as height.
        # Both are captured in the original volume calc; we can recover
        # the height from the existing volume and radii.
        if radial_build.chamber_length is not None:
            height = radial_build.chamber_length
        else:
            height = radial_build.axis_t
        bioshield_vol = calc_volume_ring(
            height, bioshield_ir, bioshield_ir + effective_thickness
        )

    # Step 4: Cost with selected material
    cost_usd = bioshield_vol * props["rho"] * props["c_raw"] * props["m"]
    cas220102.C22010203 = k_to_m_usd(cost_usd)

    # Record dose-based outputs
    cas220102.bioshield_required_thickness = Meters(required_thickness)
    cas220102.bioshield_dose_dtf = dtf
    cas220102.bioshield_material_name = material.display_name
    cas220102.bioshield_vol_safety = Meters3(bioshield_vol)
