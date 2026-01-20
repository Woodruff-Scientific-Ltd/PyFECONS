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
    rounded_cost_values = get_rounded(cost_values, 1)
    percentage_cost_values = get_percentage_cost_values(
        cost_values, costing_data.cas90.C990000, 0
    )

    # ARIES ST
    # Values from page 148, Najmabadi, F. and Aries Team, 2003. Spherical torus concept as power plants—the ARIES-ST
    #   study. Fusion Engineering and Design, 65(2), pp.143-164.
    # TODO what inflation period is this? Move to conversions.
    inflation_factor = 1.35
    # TODO - what should we name this constant and where does it come from?
    m_factor = 5285
    m30 = costing_data.cas30.C300000 / costing_data.cas90.C990000 * m_factor
    m40 = costing_data.cas40.C400000 / costing_data.cas90.C990000 * m_factor
    m50 = costing_data.cas50.C500000 / costing_data.cas90.C990000 * m_factor
    m60 = costing_data.cas60.C600000 / costing_data.cas90.C990000 * m_factor
    m99 = m_factor + m30 + m40 + m50 + m60

    # LIFE Values Anklam 2011
    # TODO this a_power is different than inputs.financial.a_power, are they supposed to be different?
    a_power = 1217  # this is the net electric power used because Anklan uses $/kWe

    life_values = {
        "M100000": 0,
        "M200000": m_factor,
        "M210000": (700 * a_power * 1000) / 1e6,
        "M220000": 2662 / inflation_factor,  # TODO is this correct
        "M220103": (1350 * a_power * 1000) / 1e6,
        "M220400": (170 * a_power * 1000) / (2 * 1e6),
        "M220500": (170 * a_power * 1000) / (2 * 1e6),
        "M220700": (100 * a_power * 1000) / 1e6,
        "M230000": (480 * a_power * 1000) / 1e6,
        "M300000": m30,
        "M400000": m40,
        "M500000": m50,
        "M600000": m60,
        "M990000": m99,
    }
    life_values_inflation = get_cost_values_inflation(life_values, inflation_factor, 2)
    life_values_percentages = get_percentage_cost_values(life_values, m99, 2)

    life_values_empty = {
        "M220100": "-",
        "M220101": "-",
        "M220102": "-",
        "M220104": "-",
        "M220105": "-",
        "M220106": "-",
        "M220107": "-",
        "M220108": "-",
        "M220109": "-",
        "M220111": "-",
        "M220119": "-",
        "M220200": "-",
        "M220300": "-",
        "M220600": "-",
        "M240000": "-",
        "M250000": "-",
        "M260000": "-",
        "M270000": "-",
        "M280000": "-",
        "M290000": "-",
    }
    life_values_empty_percentages = map_keys_to_percentage(life_values_empty)

    return (
        rounded_cost_values
        | percentage_cost_values
        | life_values_inflation
        | life_values_percentages
        | life_values_empty
        | life_values_empty_percentages
    )
