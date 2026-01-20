import math

import numpy as np

from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.categories.cas100000 import CAS10
from pyfecons.costing.safety.licensing import licensing_safety_addon
from pyfecons.enums import Region
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.tritium_release import TritiumRelease
from pyfecons.units import M_USD

# Calibration constants for CAS10 land cost model (see CAS100000.tex, 2022 update)
# These scale neutron and fusion power so that the land cost matches the
# 400 acre, $10k/acre reference plant example.
LAND_COST_POWER_NORMALIZATION_MW = 239.0
LAND_COST_SCALING_FACTOR = 0.9

# Land valuation used for tritium-driven site boundary sizing (USDA 2022
# farm real estate values, see safety analysis notes).
US_FARM_REAL_ESTATE_VALUE_USD_PER_ACRE = 3800.0

# Fraction of total tritium inventory assumed to reach the stack during
# the bounding release scenario (see Lukacs & Williams 2020 analysis).
STACK_RELEASE_FRACTION = 0.10

# Conversion from square meters to acres.
M2_TO_ACRES = 0.000247105


def _compute_tritium_land_addon(
    basic: Basic, tritium: TritiumRelease | None, baseline_land_cost: M_USD
) -> M_USD:
    """
    Safety-driven land / tritium release mitigation add-on (C110200).

    This follows the approach in the CATF safety analysis notebook
    (Lukacs & Williams 2020):
    - Use a polynomial fit for the site boundary required to stay below
      UK ERL sheltering levels for dust release at 20 m stack height.
    - Convert that boundary into a site area and land cost using
      USDA 2022 US farm real estate values.
    - Treat the resulting site cost as the safety-driven component
      C110200 that is added on top of the baseline C110100 land cost.

    Notes:
    - Only applied when include_safety_hazards_costs is True.
    - Currently implemented for Region.US only (the underlying land
      value reference is US-specific); other regions return 0 add-on
      until region-specific data are available.
    - If safety is enabled but TritiumRelease inputs are missing, we
      raise to avoid silently hiding a zero implementation.
    """

    if not getattr(basic, "include_safety_hazards_costs", False):
        return M_USD(0.0)

    if tritium is None:
        raise ValueError(
            "TritiumRelease inputs must be provided when "
            "include_safety_hazards_costs is enabled for CAS10."
        )

    # Only apply the tritium-driven land add-on for explicit US cases for
    # now, since the reference land value is US-specific.
    region = getattr(basic, "region", None)
    if region is None or region != Region.US:
        return M_USD(0.0)

    if (
        tritium.hto_inventory_g is None
        or tritium.dust_tritium_inventory_g_per_month is None
    ):
        raise ValueError(
            "TritiumRelease.hto_inventory_g and "
            "dust_tritium_inventory_g_per_month must be set when "
            "include_safety_hazards_costs is enabled for CAS10."
        )

    # For now, support the 20 m stack height case used in the analysis.
    # If a different height is provided, we conservatively clamp to 20 m
    # until additional polynomial fits are implemented.
    stack_height_m = tritium.stack_height_m or 20.0
    if abs(stack_height_m - 20.0) > 1e-6:
        stack_height_m = 20.0

    # Distance grid [m] and dust inventories [g] to trigger sheltering at
    # those distances for a 20 m stack height (Table from Lukacs &
    # Williams 2020, as encoded in catf_ongoing_changes.py).
    distance_m = np.array([0.0, 200.0, 500.0, 1000.0])
    dust_s_20_g = np.array([0.0, 831.0, 2200.0, 5000.0])

    # Fit a quadratic distance(dust) for the sheltering criterion.
    coeff_dust_to_distance = np.polyfit(dust_s_20_g, distance_m, 2)
    dust_to_distance = np.poly1d(coeff_dust_to_distance)

    # Effective dust inventory reaching the stack in the bounding release.
    dust_inv_stack_g = (
        tritium.dust_tritium_inventory_g_per_month * STACK_RELEASE_FRACTION
    )

    site_boundary_m = float(dust_to_distance(dust_inv_stack_g))
    site_boundary_m = max(site_boundary_m, 0.0)

    site_area_m2 = math.pi * site_boundary_m**2
    site_area_acres = site_area_m2 * M2_TO_ACRES
    site_cost_usd = site_area_acres * US_FARM_REAL_ESTATE_VALUE_USD_PER_ACRE
    site_cost_musd = site_cost_usd / 1e6

    total_hazard_driven_land_cost = M_USD(site_cost_musd)
    return total_hazard_driven_land_cost


def cas_10_pre_construction_costs(
    basic: Basic, power_table: PowerTable, tritium: TritiumRelease | None
) -> CAS10:
    # Cost Category 10: Pre-construction Costs
    cas10 = CAS10()

    # Cost Category 11: Land and Land Rights
    cas10.C110100 = M_USD(
        math.sqrt(basic.n_mod)
        * (
            power_table.p_neutron
            / LAND_COST_POWER_NORMALIZATION_MW
            * LAND_COST_SCALING_FACTOR
            + basic.p_nrl / LAND_COST_POWER_NORMALIZATION_MW * LAND_COST_SCALING_FACTOR
        )
    )
    # Safety-driven land / tritium release mitigation add-on
    cas10.C110200 = _compute_tritium_land_addon(basic, tritium, cas10.C110100)
    cas10.C110000 = cas10.C110100 + cas10.C110200

    # Cost Category 12 – Site Permits
    cas10.C120000 = M_USD(10)

    # Cost Category 13 – Plant Licensing
    # Base cost from 'Capital Costs' section of
    # https://world-nuclear.org/information-library/economic-aspects/economics-of-nuclear-power.aspx
    base_licensing_cost = M_USD(210)
    # Safety and hazard mitigation addon (region-dependent, applied when enabled)
    cas10.C130000 = base_licensing_cost + licensing_safety_addon(basic)

    # Cost Category 14 – Plant Permits
    cas10.C140000 = M_USD(5)

    # Cost Category 15 – Plant Studies
    cas10.C150000 = M_USD(5)

    # Cost Category 16 – Plant Reports
    cas10.C160000 = M_USD(2)

    # Cost Category 17 – Other Pre-Construction Costs
    cas10.C170000 = M_USD(1)

    # Cost Category 19 - Contingency
    if basic.noak:
        cas10.C190000 = M_USD(0)
    else:
        cas10.C190000 = M_USD(
            0.1
            * (
                cas10.C110000
                + cas10.C120000
                + cas10.C130000
                + cas10.C140000
                + cas10.C150000
                + cas10.C160000
                + cas10.C170000
            )
        )

    # Cost Category 10
    cas10.C100000 = M_USD(
        cas10.C110000
        + cas10.C120000
        + cas10.C130000
        + cas10.C140000
        + cas10.C150000
        + cas10.C160000
        + cas10.C170000
        + cas10.C190000
    )

    return cas10
