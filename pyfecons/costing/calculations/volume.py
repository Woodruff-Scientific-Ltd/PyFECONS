import numpy as np

from pyfecons.units import Meters, Meters3


def calc_volume_sphere(inner: float, outer: float) -> float:
    return 4 / 3 * np.pi * (outer**3 - inner**3)


def calc_volume_ring(height: float, inner: float, outer: float) -> float:
    return Meters3(height * np.pi * (outer**2 - inner**2))


def calc_volume_outer_hollow_torus(
    axis_t: Meters, inner: Meters, thickness: Meters
) -> Meters3:
    """
    Volume of the outer surface of a hollow torus defined by:

    axis_t = major radius
    thickness = thickness in minor radius of the hollow torus
    inner = the "inner radius" of the follow torus on the outboard side.

    so the minor radius "a" of the outer part of the hollow torus is:

        a = inner - axis_t + thickness.
    """
    return Meters3(2 * np.pi * axis_t * np.pi * (inner - axis_t + thickness) ** 2)
