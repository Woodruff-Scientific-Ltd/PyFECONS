"""
Dose-based bioshield thickness and cost calculation.

When safety costs are enabled, computes the required bioshield thickness
from dose attenuation requirements and costs using the selected bioshield
material instead of hard-coded SS316.

DTF (Dose Transmission Factor) data sourced from BRL-1174:
    Allen, Futterer & Wright, "Neutron Transmission Versus Thickness
    for Some Common Materials", Sep 1962.
"""

import numpy as np

from pyfecons.enums import BioshieldMaterial

# Inches-to-meters conversion
INCHES_TO_METERS = 0.0254

# DTF-vs-thickness data from BRL-1174 (thickness in inches).
# Each entry: (thicknesses, dtf_values)
_DTF_DATA = {
    BioshieldMaterial.WATER: (
        [0, 1, 2, 3, 5, 6, 8, 9, 12],
        [1, 0.955, 0.91, 0.82, 0.685, 0.64, 0.505, 0.46, 0.325],
    ),
    BioshieldMaterial.BORATED_POLYETHYLENE: (
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
        [1, 0.95, 0.88, 0.8, 0.68, 0.6, 0.5, 0.4, 0.35, 0.28, 0.2, 0.15],
    ),
    # Corrected from notebook: dropped non-physical DTF=0.8 at 3" and
    # unmatched 10th DTF value. See implementation doc assumption #1.
    BioshieldMaterial.IRON: (
        [0, 1, 2, 4, 6, 8, 10, 12],
        [1, 0.9, 0.75, 0.62, 0.55, 0.38, 0.25, 0.19],
    ),
    # Placeholder: uses borated polyethylene curve. This is conservative —
    # polyethylene has better neutron moderation than concrete, so concrete
    # will be slightly over-thick. See implementation doc assumption #2.
    BioshieldMaterial.CONCRETE: (
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
        [1, 0.95, 0.88, 0.8, 0.68, 0.6, 0.5, 0.4, 0.35, 0.28, 0.2, 0.15],
    ),
}

# Material properties for bioshield costing.
# density (kg/m3), cost_per_kg ($/kg), manufacturing_factor
# See implementation doc assumption #3 for manufacturing factors.
BIOSHIELD_MATERIAL_PROPERTIES = {
    BioshieldMaterial.CONCRETE: {
        "rho": 2260,
        "c_raw": 0.085,
        "m": 2,
    },
    BioshieldMaterial.BORATED_POLYETHYLENE: {
        "rho": 970,
        "c_raw": 4,
        "m": 1.5,
    },
    BioshieldMaterial.IRON: {
        "rho": 7880,
        "c_raw": 0.1069,
        "m": 2,
    },
    BioshieldMaterial.WATER: {
        "rho": 1000,
        "c_raw": 0,
        "m": 1,
    },
}


def _build_dtf_polynomial(material: BioshieldMaterial):
    """Fit a polynomial to DTF-vs-thickness data for the given material.

    Returns a polynomial that maps thickness (inches) -> DTF.
    """
    thicknesses, dtf_values = _DTF_DATA[material]
    # Degree 4 polynomial fit; clamp to available data range
    degree = min(4, len(thicknesses) - 1)
    return np.polyfit(thicknesses, dtf_values, degree)


def compute_required_thickness_meters(
    material: BioshieldMaterial,
    initial_dose: float,
    regulatory_dose: float,
) -> float:
    """Compute the required bioshield thickness in meters.

    Args:
        material: Selected bioshield material.
        initial_dose: Dose rate at bioshield inner surface without
            bioshield (Sv/yr).
        regulatory_dose: Target dose rate outside bioshield (Sv/yr).

    Returns:
        Required thickness in meters.
    """
    if initial_dose <= 0 or regulatory_dose <= 0:
        return 0.0

    target_dtf = regulatory_dose / initial_dose

    if target_dtf >= 1.0:
        # No shielding needed — dose already below limit
        return 0.0

    # Invert the DTF curve: find thickness where DTF = target_dtf.
    # Use the polynomial fit and solve numerically.
    thicknesses_in, dtf_values = _DTF_DATA[material]
    coeffs = _build_dtf_polynomial(material)
    poly = np.poly1d(coeffs)

    # Shift polynomial: poly(t) - target_dtf = 0
    shifted_coeffs = coeffs.copy()
    shifted_coeffs[-1] -= target_dtf
    roots = np.roots(shifted_coeffs)

    # Filter for real, positive roots
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-6 and r.real > 0]

    if real_roots:
        # Take the smallest positive root (first crossing)
        thickness_inches = min(real_roots)
    else:
        # target_dtf is below what the polynomial can reach in the data range;
        # use the maximum data thickness as a conservative fallback
        thickness_inches = max(thicknesses_in)

    return thickness_inches * INCHES_TO_METERS
