import numpy as np
from pyfecons.units import Meters3


def calc_volume_sphere(inner: float, outer: float) -> float:
    return 4/3 * np.pi * (outer**3 - inner**3)


def calc_volume_ring(height: float, outer: float, inner: float) -> float:
    return Meters3(height * np.pi * (outer ** 2 - inner ** 2))


def calc_volume_torus(radius: float, inner: float, outer: float):
    return Meters3(2 * np.pi * radius * np.pi * (inner + outer) ** 2)
