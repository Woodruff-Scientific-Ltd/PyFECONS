import numpy as np
from typing import List, Tuple, Callable
from scipy.interpolate import interp1d


def interpolate_data(coordinates: List[Tuple[float, float]]
                     ) -> Callable[[float], np.ndarray]:
    """
    Creates an interpolation function from coordinates.

    Parameters:
    - coordinates (List[Tuple[float, float]]): A list of (x, y) tuples.

    Returns:
    - Callable[[float], np.ndarray]: An interpolation function that accepts a float and returns a numpy array.
    """
    x = [coord[0] for coord in coordinates]
    y = [coord[1] for coord in coordinates]
    return interp1d(x, y, kind='linear', fill_value="extrapolate")


def get_interpolated_value(interpolation_function: Callable[[float], np.ndarray]
                           , frequency: float) -> float:
    """
    Returns the interpolated value for a given frequency using the provided interpolation function.

    Parameters:
    - interpolation_function (Callable[[float], np.ndarray]): The function to use for interpolation.
    - frequency (float): The frequency at which to find the interpolated value.

    Returns:
    - float: The interpolated value as a float.
    """
    return interpolation_function(frequency).item()