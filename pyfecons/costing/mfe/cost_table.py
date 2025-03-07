from pyfecons.costing.calculations.cost_table_builder import (
    get_cost_values,
    get_rounded,
    get_percentage_cost_values,
    get_cost_values_inflation,
    map_keys_to_percentage,
)
from pyfecons.data import Data, CostTable


def cost_table(data: Data) -> CostTable:
    # Cost Table
    cost_table = CostTable()
    cost_values = get_cost_values(data)
    rounded_cost_values = get_rounded(cost_values, 2)
    percentage_cost_values = get_percentage_cost_values(
        cost_values, data.cas90.C990000, 2
    )

    # ARIES ST
    # Values from page 148, Najmabadi, F. and Aries Team, 2003. Spherical torus concept as power plants—the ARIES-ST
    #   study. Fusion Engineering and Design, 65(2), pp.143-164.
    # TODO what inflation period is this? Move to conversions.
    inflation_factor = 1.35
    # TODO can we name the value 4479.7?
    m_factor = 4479.7
    m30 = data.cas30.C300000 / data.cas90.C990000 * m_factor
    m40 = data.cas40.C400000 / data.cas90.C990000 * m_factor
    m50 = data.cas50.C500000 / data.cas90.C990000 * m_factor
    m60 = data.cas60.C600000 / data.cas90.C990000 * m_factor
    m99 = m_factor + m30 + m40 + m50 + m60

    # LIFE Values Anklam 2011
    # TODO this a_power is different than inputs.financial.a_power, are they supposed to be different?
    a_power = 2920  # this is the net electric power - TODO this is not used

    aries_st_values = {
        "M100000": 10.6,
        "M200000": m_factor,
        "M210000": 370.8,
        "M220000": 1244.1,
        "M220100": 648.7,
        "M220101": 50.2,
        "M220102": 113.1,
        "M220103": 102.6,
        "M220104": 212.5,
        "M220105": 37.4,
        "M220106": 48.1,
        "M220107": 71.6,
        "M220108": 8.8,
        "M220119": 358,
        "M2207": 3.49,
        "M23": 339,
        "M24": 125.4,
        "M25": 77.9,
        "M26": 64.3,
        "M27": 108.9,
        "M29": 555.1,
        "M30": m30,
        "M40": 429,
        "M50": m50,
        "M60": m60,
        "M99": m99,
    }

    aries_st_empty_values = {
        "M220109": "-",
        "M220111": "-",
        "M2202": "-",
        "M2203": "-",
        "M2204": "-",
        "M2205": "-",
        "M2206": "-",
        "M28": "-",
    }

    aries_st_values_inflation = get_cost_values_inflation(
        aries_st_values, inflation_factor, 2
    )
    aries_st_percentages = get_percentage_cost_values(aries_st_values, m99, 2)
    aries_st_empty_percentages = map_keys_to_percentage(aries_st_empty_values)

    cost_table.template_file = "CASstructure.tex"
    cost_table.replacements = (
        rounded_cost_values
        | percentage_cost_values
        | aries_st_values_inflation
        | aries_st_percentages
        | aries_st_empty_values
        | aries_st_empty_percentages
    )
    return cost_table
