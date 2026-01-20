from pyfecons.costing_data import CostingData
from pyfecons.report.cost_table.cost_table_builder import (
    get_cost_values,
    get_cost_values_inflation,
    get_percentage_cost_values,
    get_rounded,
    map_keys_to_percentage,
)


def get_replacements(costing_data: CostingData) -> dict[str, str]:
    # Cost Table
    cost_values = get_cost_values(costing_data)
    rounded_cost_values = get_rounded(cost_values, 2)
    percentage_cost_values = get_percentage_cost_values(
        cost_values, costing_data.cas90.C990000, 2
    )

    # ARIES ST
    # Values from page 148, Najmabadi, F. and Aries Team, 2003. Spherical torus concept as power plants—the ARIES-ST
    #   study. Fusion Engineering and Design, 65(2), pp.143-164.
    # TODO what inflation period is this? Move to conversions.
    inflation_factor = 1.35
    # TODO can we name the value 4479.7?
    m_factor = 4479.7
    m30 = costing_data.cas30.C300000 / costing_data.cas90.C990000 * m_factor
    m40 = costing_data.cas40.C400000 / costing_data.cas90.C990000 * m_factor
    m50 = costing_data.cas50.C500000 / costing_data.cas90.C990000 * m_factor
    m60 = costing_data.cas60.C600000 / costing_data.cas90.C990000 * m_factor
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
        "M220200": 358,
        "M220300": 0,
        "M220400": 0,
        "M220500": 0,
        "M220600": 0,
        "M220700": 3.49,
        "M230000": 339,
        "M240000": 125.4,
        "M250000": 77.9,
        "M260000": 64.3,
        "M270000": 108.9,
        "M280000": 0,
        "M290000": 555.1,
        "M300000": m30,
        "M400000": 429,
        "M500000": m50,
        "M600000": m60,
        "M990000": m99,
    }

    aries_st_empty_values = {
        "M220109": "-",
        "M220111": "-",
        "M220120": "-",
        "M220606": "-",
    }

    aries_st_values_inflation = get_cost_values_inflation(
        aries_st_values, inflation_factor, 2
    )
    aries_st_percentages = get_percentage_cost_values(aries_st_values, m99, 2)
    aries_st_empty_percentages = map_keys_to_percentage(aries_st_empty_values)

    return (
        rounded_cost_values
        | percentage_cost_values
        | aries_st_values_inflation
        | aries_st_percentages
        | aries_st_empty_values
        | aries_st_empty_percentages
    )
