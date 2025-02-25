from dataclasses import dataclass

from pyfecons.units import Ratio, Meters


@dataclass
class RadialBuild:
    # Radial build inputs
    elon: Ratio = None  # torus elongation factor
    chamber_length: Meters = None  # chamber length
    # Radial thicknesses of concentric components (innermost to outermost)
    axis_t: Meters = (
        None  # distance from axis of symmetry at R=0 to the plasma major radius
    )
    plasma_t: Meters = None  # plasma radial thickness
    vacuum_t: Meters = None  # vacuum radial thickness
    firstwall_t: Meters = None  # first wall radial thickness
    blanket1_t: Meters = None  # blanket radial thickness
    reflector_t: Meters = None  # reflector radial thickness
    ht_shield_t: Meters = None  # High-temperature shield radial thickness
    structure_t: Meters = None  # support structure radial thickness
    gap1_t: Meters = None  # air gap radial thickness
    vessel_t: Meters = None  # vacuum vessel wall radial thickness
    coil_t: Meters = None  # TF coil radial thickness
    gap2_t: Meters = None  # second air gap radial thickness
    lt_shield_t: Meters = None  # low-temperature shield radial thickness
    bioshield_t: Meters = None  # concrete bioshield radial thickness
