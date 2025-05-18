from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.categories.cas500000 import CAS50
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD


def cas50_capitalized_supplementary_costs(
    basic: Basic, power_table: PowerTable, cas23_to_28_total_cost: M_USD
) -> CAS50:
    # Cost Category 50 Capitalized Supplementary Costs (CSC)
    # TODO determine cost basis, ask simon
    cas50 = CAS50()

    # TODO - should all of these constants be optional input estimates?
    # Cost Category 51 – Shipping and Transportation Costs
    cas50.C510000 = M_USD(8)

    # Cost Category 52 – Spare Parts
    # TODO - justification for this calculation?
    cas50.C520000 = M_USD(0.1 * cas23_to_28_total_cost)

    # Cost Category 53 – Taxes
    cas50.C530000 = M_USD(100)

    # Cost Category 54 – Insurance
    cas50.C540000 = M_USD(1)

    # Cost Category 55 – Initial Fuel Load
    # $22 M to $34 M (2016 USD) for a standard 150 MWe FPP.
    cas50.C550000 = M_USD(power_table.p_net / 150 * 34)

    # Cost Category 58 – Decommissioning Costs
    cas50.C580000 = M_USD(200)

    # Cost Category 59 – Contingency on Supplementary Costs
    if basic.noak:
        cas50.C590000 = M_USD(0)
    else:
        cas50.C590000 = M_USD(
            0.1
            * (
                cas50.C580000
                + cas50.C550000
                + cas50.C540000
                + cas50.C530000
                + cas50.C520000
                + cas50.C510000
            )
        )

    cas50.C500000 = M_USD(
        cas50.C510000
        + cas50.C520000
        + cas50.C530000
        + cas50.C540000
        + cas50.C550000
        + cas50.C580000
        + cas50.C590000
    )
    return cas50
