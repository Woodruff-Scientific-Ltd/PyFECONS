"""Disruption mitigation system cost calculation.

This module calculates the cost of the shattered pellet injection system
used to mitigate plasma disruption effects in tokamak fusion reactors.

Cost Basis:
- ITER Engineering Design Activities Final Report (2001)
- Cost: 5.66433 kIUA (kilo ITER Unit of Account)
- 1 IUA = USD 1,000 (January 1989 value)
- Base cost: 5,664,330 USD (1989 dollars)

Reference:
Baylor, L.R., Meitner, S.J., Gebhart, T.E., Caughman, J.B.O., Herfindal, J.L.,
Shiraki, D. and Youchison, D.L., 2019. Shattered pellet injection technology
design and characterization for disruption mitigation experiments. Nuclear fusion,
59(6), p.066008.
"""

from pyfecons.costing.categories.cas220120 import CAS220120
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def cas_220120_disruption_mitigation_costs(basic: Basic) -> CAS220120:
    """Calculate Cost Category 22.01.20: Disruption Mitigation System.

    This cost is only applicable to MFE (magnetic fusion energy) reactors,
    specifically tokamak designs that require disruption mitigation systems.

    Args:
        basic: Basic configuration inputs including inflation rate and safety flag

    Returns:
        CAS220120: Cost category data with disruption mitigation system cost

    Note:
        Cost is only included if include_safety_hazards_costs is True in basic config.
        If False, returns zero cost.
    """
    cas220120 = CAS220120()

    # Only calculate if safety hazards costs are enabled
    if not basic.include_safety_hazards_costs:
        cas220120.C220120 = M_USD(0.0)
        return cas220120

    # Base cost from ITER design (1989 dollars)
    # 5.66433 kIUA * 1000 USD/IUA = 5,664,330 USD
    base_cost_1989_usd = 5.66433 * 1000 * 1000

    # Apply inflation from 1989 to current year
    # Calculate years from 1989 to current (assuming construction_time or similar)
    # For now, use yearly_inflation rate if available
    if basic.yearly_inflation is not None:
        # Approximate years from 1989 to 2024 (35 years) as baseline
        # In practice, this could be calculated from construction_time or current year
        years_from_1989 = 35  # 2024 - 1989
        inflation_factor = (1 + basic.yearly_inflation) ** years_from_1989
        current_cost_usd = base_cost_1989_usd * inflation_factor
    else:
        # If no inflation rate provided, use a default inflation factor
        # Average US inflation ~2.5% per year from 1989-2024
        default_inflation_rate = 0.025
        years_from_1989 = 35
        inflation_factor = (1 + default_inflation_rate) ** years_from_1989
        current_cost_usd = base_cost_1989_usd * inflation_factor

    # Convert to millions USD
    cas220120.C220120 = M_USD(current_cost_usd / 1e6)

    return cas220120
