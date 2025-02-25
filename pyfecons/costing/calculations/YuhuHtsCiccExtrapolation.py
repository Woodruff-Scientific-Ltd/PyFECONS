import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator
from sklearn.linear_model import LinearRegression

from pyfecons.inputs.magnet import Magnet

# noinspection PyTypeChecker
yuhudata = {
    "R_Turns": [31] * 6
    + [44] * 6
    + [54] * 6
    + [63] * 6
    + [70] * 6
    + [77] * 6
    + [83] * 6
    + [89] * 6
    + [94] * 6,
    "Z_Turns": [31] * 6
    + [44] * 6
    + [54] * 6
    + [63] * 6
    + [70] * 6
    + [77] * 6
    + [83] * 6
    + [89] * 6
    + [94] * 6,
    "Single cable I (A)": [6995.627628] * 54,
    "r_av(m)": [2, 4, 6, 8, 10, 12] * 9,
    "z_av(m)": [0] * 54,
    "dr(m)": [0.49] * 6
    + [0.69] * 6
    + [0.84] * 6
    + [0.98] * 6
    + [1.09] * 6
    + [1.19] * 6
    + [1.29] * 6
    + [1.38] * 6
    + [1.46] * 6,
    "dz(m)": [0.49] * 6
    + [0.69] * 6
    + [0.84] * 6
    + [0.98] * 6
    + [1.09] * 6
    + [1.19] * 6
    + [1.29] * 6
    + [1.38] * 6
    + [1.46] * 6,
    "B_mag": [
        2.10616637,
        1.055303175,
        0.7038001463,
        0.5279190692,
        0.4223607165,
        0.3519787731,
        4.231018337,
        2.124598537,
        1.417450588,
        1.063360003,
        0.8507881835,
        1.067875207,
        6.354170539,
        3.198019278,
        2.134370652,
        1.601384033,
        1.281329818,
        1.067875207,
        8.619030499,
        4.349716057,
        2.904216973,
        2.179287368,
        1.743841805,
        1.453386963,
        10.60629681,
        5.36649644,
        3.584455229,
        2.690064162,
        2.152680752,
        1.794183669,
        12.79002712,
        6.48913364,
        4.335975808,
        3.254475088,
        2.604488795,
        2.170815472,
        14.80337025,
        7.534262639,
        5.036490264,
        3.780787985,
        3.025873763,
        2.522119182,
        16.95437589,
        8.656634754,
        5.789240305,
        4.34645187,
        3.478801173,
        2.899735523,
        18.84016525,
        9.649873196,
        6.456142837,
        4.84777952,
        3.880275834,
        3.234481465,
    ],
}


# Function to fit linear regression model for extrapolation
def fit_linear_regression(x, y):
    model = LinearRegression()
    model.fit(x, y)
    return model


# Function to interpolate or extrapolate
def interpolate_or_extrapolate(
    model_interp, model_regr, x_new, buffer_ratio=0.1, override_checks=False
):
    """
    This function attempts to interpolate first, and if the value falls outside of the interpolation range,
    then tries to extrapolate within a dynamically calculated buffer beyond the known data range.
    The range checks can be overridden if necessary.
    """
    # Ensure x_new is two-dimensional
    if (
        x_new.ndim != 2 or x_new.shape[1] != 2
    ):  # Correcting for standard two features input
        raise ValueError(
            "X_new must be a two-dimensional array with shape (n_samples, n_features)."
        )

    # Try to interpolate
    interp_val = model_interp(x_new)
    if not np.isnan(interp_val):  # Check if interpolation was successful
        return interp_val
    else:
        # Dynamically adjust the allowed extrapolation range based on actual data range and a buffer ratio
        extrapolation_ranges = [
            (
                model_regr.data_range_[i][0]
                - (model_regr.data_range_[i][1] - model_regr.data_range_[i][0])
                * buffer_ratio,
                model_regr.data_range_[i][1]
                + (model_regr.data_range_[i][1] - model_regr.data_range_[i][0])
                * buffer_ratio,
            )
            for i in range(len(model_regr.data_range_))
        ]

        # Check if X_new is within the dynamically adjusted extrapolation range, unless override is active
        if not override_checks:
            for i, (value, (min_val, max_val)) in enumerate(
                zip(x_new[0], extrapolation_ranges)
            ):
                if not (min_val <= value <= max_val):
                    print(
                        f"Warning: Attempted extrapolation beyond dynamically adjusted range for feature {i}."
                    )
                    return None

        # If within the adjusted range or override is active, perform extrapolation
        return float(model_regr.predict(x_new)[0])  # Ensure predict is called correctly


"""
HTS CICC AUTO GENERATION OF DESIGN PARAMETERS FROM YUHU ZHAI EXTRAPOLATION
"""


class YuhuHtsCiccExtrapolation:
    def __init__(self, magnet: Magnet, override_checks: bool):
        df_new = pd.DataFrame(yuhudata)

        # Extracting necessary columns from data frame for interpolation
        interp_data = df_new[
            [
                "B_mag",
                "r_av(m)",
                "R_Turns",
                "Z_Turns",
                "Single cable I (A)",
                "dr(m)",
                "dz(m)",
            ]
        ]

        # Preparing the interpolators for each output variable
        rTurnsCICC_interp = LinearNDInterpolator(
            interp_data[["B_mag", "r_av(m)"]].values, interp_data["R_Turns"]
        )
        zTurnsCICC_interp = LinearNDInterpolator(
            interp_data[["B_mag", "r_av(m)"]].values, interp_data["Z_Turns"]
        )
        cableCurrentCICC_interp = LinearNDInterpolator(
            interp_data[["B_mag", "r_av(m)"]].values, interp_data["Single cable I (A)"]
        )
        drCICC_interp = LinearNDInterpolator(
            interp_data[["B_mag", "r_av(m)"]].values, interp_data["dr(m)"]
        )
        dzCICC_interp = LinearNDInterpolator(
            interp_data[["B_mag", "r_av(m)"]].values, interp_data["dz(m)"]
        )

        # Fitting models
        X = interp_data[["B_mag", "r_av(m)"]].values
        models = {
            "R_Turns": fit_linear_regression(X, interp_data["R_Turns"]),
            "Z_Turns": fit_linear_regression(X, interp_data["Z_Turns"]),
            "Single cable I (A)": fit_linear_regression(
                X, interp_data["Single cable I (A)"]
            ),
            "dr(m)": fit_linear_regression(X, interp_data["dr(m)"]),
            "dz(m)": fit_linear_regression(X, interp_data["dz(m)"]),
        }

        self.x_new = np.array(
            [[magnet.auto_cicc_b, magnet.auto_cicc_r]]
        )  # Adjusted for your new data
        self.override_checks = (
            override_checks  # Set this to True to bypass the range checks
        )
        self.r_turns = interpolate_or_extrapolate(
            rTurnsCICC_interp,
            models["R_Turns"],
            self.x_new,
            override_checks=override_checks,
        )
        self.z_turns = interpolate_or_extrapolate(
            zTurnsCICC_interp,
            models["Z_Turns"],
            self.x_new,
            override_checks=override_checks,
        )
        self.cable_current = interpolate_or_extrapolate(
            cableCurrentCICC_interp,
            models["Single cable I (A)"],
            self.x_new,
            override_checks=override_checks,
        )
        self.dr = interpolate_or_extrapolate(
            drCICC_interp, models["dr(m)"], self.x_new, override_checks=override_checks
        )
        self.dz = interpolate_or_extrapolate(
            dzCICC_interp, models["dz(m)"], self.x_new, override_checks=override_checks
        )
