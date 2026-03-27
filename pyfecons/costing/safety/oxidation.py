"""
Rapid structural oxidation — first wall coating cost calculation.

Evaluates whether the structural material's oxidation margin requires a
protective tungsten first wall coating. The Relative Consequence Index (RCI)
compares the material's oxidation margin to the reference case (HT-9).

Reference: Piet, Kazimi & Lidsky (1982), "Potential Consequences of Tokamak
Fusion Reactor Accidents: The Materials Impact".
"""

import math

from pyfecons.enums import BlanketStructure, ConfinementType, FusionMachineType
from pyfecons.materials import Materials

materials = Materials()

# Operating temperature T_o (°C) and oxidation onset temperature T_lt (°C)
# per structural material. Source: Piet et al. (1982), notebook values.
OXIDATION_PROPERTIES = {
    BlanketStructure.STAINLESS_STEEL_SS: {"T_o": 450, "T_lt": 1010},
    BlanketStructure.FERRITIC_MARTENSITIC_STEEL_FMS: {"T_o": 450, "T_lt": 1400},
    BlanketStructure.OXIDE_DISPERSION_STRENGTHENED_ODS_STEEL: {
        "T_o": 450,
        "T_lt": 1400,
    },  # Proxy: same as FMS (both ferritic)
    BlanketStructure.VANADIUM: {"T_o": 600, "T_lt": 700},
}

# Reference case: HT-9 (ferritic martensitic steel)
_REF_T_O = 450
_REF_T_LT = 1400
REF_MARGIN = _REF_T_LT - _REF_T_O  # 950°C


def compute_rci(structure: BlanketStructure) -> float:
    """Compute the Relative Consequence Index for oxidation.

    RCI = reference_margin / material_margin
    RCI > 1 means worse margin than HT-9 → coating needed.
    RCI < 0 means T_lt < T_o (material oxidizes below operating temp) → coating needed.
    RCI <= 1 and RCI > 0 means margin >= HT-9 → no coating needed.

    Returns:
        RCI value. float('inf') if margin is zero.
    """
    props = OXIDATION_PROPERTIES.get(structure)
    if props is None:
        return 0.0  # Unknown material, no coating

    margin = props["T_lt"] - props["T_o"]
    if margin == 0:
        return float("inf")

    return REF_MARGIN / margin


def coating_required(rci: float) -> bool:
    """Returns True if a tungsten coating is needed based on the RCI."""
    return rci > 1 or rci < 0


def compute_fw_surface_area(
    fusion_machine_type: FusionMachineType,
    confinement_type: ConfinementType,
    firstwall_ir: float,
    axis_t: float = None,
    elon: float = None,
    chamber_length: float = None,
) -> float:
    """Compute first wall inner surface area in m².

    Args:
        fusion_machine_type: MFE or IFE.
        confinement_type: Tokamak, mirror, etc.
        firstwall_ir: First wall inner radius (m).
        axis_t: Major radius (m), for tokamak.
        elon: Elongation factor, for tokamak.
        chamber_length: Chamber length (m), for mirror.

    Returns:
        Surface area in m².
    """
    if fusion_machine_type == FusionMachineType.IFE:
        # Sphere: 4π × r²
        return 4 * math.pi * firstwall_ir**2
    elif confinement_type == ConfinementType.MAGNETIC_MIRROR:
        # Cylinder: 2π × r × L
        return 2 * math.pi * firstwall_ir * chamber_length
    else:
        # Tokamak torus: surface area ≈ 4π² × R × a × κ
        # where R = major radius, a = minor radius at FW, κ = elongation
        minor_radius = firstwall_ir - axis_t
        elongation = elon if elon else 1.0
        return 4 * math.pi**2 * axis_t * minor_radius * elongation


def compute_coating_cost_usd(
    surface_area: float,
    coating_thickness: float = 0.002,
    application_cost_factor: float = 1.0,
) -> float:
    """Compute tungsten first wall coating cost in USD.

    Cost model from notebook:
      material_cost = volume × W.rho × W.c_raw
      application_cost = material_cost × application_cost_factor
      rd_cost = material_cost × 0.5
      total = material + application + R&D

    Args:
        surface_area: First wall surface area (m²).
        coating_thickness: Coating thickness (m). Default 2 mm per Cui et al. (2021).
        application_cost_factor: Application cost as fraction of material cost.
            Default 1.0 (100%, plasma spray).

    Returns:
        Total coating cost in USD.
    """
    coating_volume = surface_area * coating_thickness
    material_cost = coating_volume * materials.W.rho * materials.W.c_raw
    application_cost = material_cost * application_cost_factor
    rd_cost = material_cost * 0.5
    return material_cost + application_cost + rd_cost
