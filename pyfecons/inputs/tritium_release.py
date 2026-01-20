from dataclasses import dataclass


@dataclass
class TritiumRelease:
    """
    Parameters related to radioactive release of tritium from storage.

    All values are annual or steady-state quantities used to estimate
    region- and design-dependent insurance / licensing / land costs
    associated with tritium management.
    """

    # Tritium inventory in the form of tritiated water (HTO), in grams.
    # This typically represents the mobilizable HTO inventory relevant
    # to off-site release scenarios.
    hto_inventory_g: float | None = None

    # Tritium content in dust mobilized per month, in grams/month.
    dust_tritium_inventory_g_per_month: float | None = None

    # Effective stack height for releases to atmosphere, in meters.
    stack_height_m: float | None = None
