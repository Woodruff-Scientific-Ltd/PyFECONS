from pyfecons.costing.categories.cas780000 import CAS780000
from pyfecons.enums import Region
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.lsa_levels import LsaLevels
from pyfecons.units import M_USD

# US nuclear liability insurance premium baseline (2024, single-unit reactor site)
# Source: NRC fact sheet (referenced in CATF safety analysis notebook)
FISSION_BASELINE_ANNUAL_PREMIUM_USD = 1_100_000.0

# Fusion insurance risk factors (as fraction of fission premium), based on CATF colab estimate
# LSA 2 -> ~19% of fission risk, LSA 3 -> ~23% of fission risk
LSA_RISK_FRACTION = {
    1: 0.19,
    2: 0.19,
    3: 0.23,
    4: 0.23,
}


def cas_780000_insurance_costs(basic: Basic, lsa_levels: LsaLevels) -> CAS780000:
    """
    Annual insurance premium for Cost Category 78 – Taxes and Insurance.

    This is modeled as an annual cost (M USD/year) and is added into CAS70 (annualized O&M)
    when safety and hazard mitigation costs are enabled.
    """
    cas780000 = CAS780000()

    if not basic.include_safety_hazards_costs:
        cas780000.C780000 = M_USD(0.0)
        return cas780000

    # If region is not specified, do not assume a value
    if basic.region in (None, Region.UNSPECIFIED):
        cas780000.C780000 = M_USD(0.0)
        return cas780000

    lsa = getattr(lsa_levels, "lsa", None)
    risk_fraction = LSA_RISK_FRACTION.get(lsa, 0.23)

    annual_premium_usd = FISSION_BASELINE_ANNUAL_PREMIUM_USD * risk_fraction
    cas780000.C780000 = M_USD(annual_premium_usd / 1e6)
    return cas780000
