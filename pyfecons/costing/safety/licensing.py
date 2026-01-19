from pyfecons.enums import Region
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD

# Cost estimates derived from CATF safety analysis notebook
# US: midpoint of lower and upper bound estimates for licensing byproduct materials
US_LOWER_LICENSING_COST_USD = 26_708_000.0
US_UPPER_LICENSING_COST_USD = 80_323_680.0
US_AVG_LICENSING_COST_USD = (
    US_LOWER_LICENSING_COST_USD + US_UPPER_LICENSING_COST_USD
) / 2.0

# UK: total licensing cost under REPPIR 2019 and EA charges (~£55k), approximated in USD
UK_LICENSING_COST_USD = 70_000.0


def licensing_safety_addon(basic: Basic) -> M_USD:
    """
    Additional licensing cost for Cost Category 13 – Plant Licensing,
    applied when safety and hazard mitigation costs are enabled.

    This cost is region-dependent and is added on top of the baseline
    licensing cost already included in CAS10.

    Returns 0 if region is UNSPECIFIED or safety costs are disabled.
    """
    if not basic.include_safety_hazards_costs:
        return M_USD(0.0)

    region = basic.region or Region.UNSPECIFIED

    if region == Region.UK:
        cost_usd = UK_LICENSING_COST_USD
    elif region == Region.US:
        cost_usd = US_AVG_LICENSING_COST_USD
    else:  # UNSPECIFIED or unknown region
        return M_USD(0.0)

    # Convert to millions of USD
    return M_USD(cost_usd / 1e6)
