from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    OUT = data.cas50

    # Cost Category 50 Capitalized Supplementary Costs (CSC)

    # Cost Category 51 – Shipping and Transportation Costs
    OUT.C510000 = M_USD(8)

    # Cost Category 52 – Spare Parts
    OUT.C520000 = M_USD(0.1 * (data.cas23.C230000 + data.cas24.C240000 + data.cas25.C250000
                               + data.cas26.C260000 + data.cas27.C270000 + data.cas28.C280000))

    # Cost Category 53 – Taxes
    OUT.C530000 = M_USD(100)

    # Cost Category 54 – Insurance
    OUT.C540000 = M_USD(1)

    # Cost Category 55 – Initial Fuel Load
    # $22 M to $34 M (2016 USD) for a standard 150 MWe FPP.
    OUT.C550000 = M_USD(data.power_table.p_net / 150 * 34)

    # Cost Category 58 – Decommissioning Costs
    OUT.C580000 = M_USD(200)

    # Cost Category 59 – Contingency on Supplementary Costs
    if inputs.basic.noak:
        OUT.C590000 = M_USD(0)
    else:
        OUT.C590000 = M_USD(0.1 * (OUT.C580000 + OUT.C550000 + OUT.C540000 + OUT.C530000 + OUT.C520000 + OUT.C510000))

    OUT.C500000 = M_USD(OUT.C510000 + OUT.C520000 + OUT.C530000 + OUT.C540000 + OUT.C550000
                        + OUT.C580000 + OUT.C590000)