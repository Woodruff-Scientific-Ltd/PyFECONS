from pyfecons.costing.categories.cas900000 import CAS90
from pyfecons.inputs.financial import Financial
from pyfecons.units import M_USD


def cas90_annualized_financial_costs(
    financial: Financial, cas10_to_60_total_capital_cost: M_USD
) -> CAS90:
    # Cost Category 90: Annualized Financial Costs (AFC)
    cas90 = CAS90()

    # Total Capital costs 99
    cas90.C990000 = cas10_to_60_total_capital_cost

    cas90.C900000 = M_USD(financial.capital_recovery_factor * cas90.C990000)
    return cas90
