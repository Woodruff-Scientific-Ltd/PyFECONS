from pyfecons.costing.calculations.cost_table_builder import get_cost_values, get_rounded, get_percentage_cost_values, \
    get_cost_values_inflation, map_keys_to_percentage
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def GenerateData(inputs: Inputs, data: Data) -> list[TemplateProvider]:
    # Cost Table
    OUT = data.cost_table
    cost_values = get_cost_values(data)
    rounded_cost_values = get_rounded(cost_values, 1)
    percentage_cost_values = get_percentage_cost_values(cost_values, data.cas90.C990000, 0)
    inflation_factor = 1.35  # TODO move to conversions and do the same in MFE

    # TODO - what should we name this constant and where does it come from?
    m_factor = 5285
    m30 = data.cas30.C300000 / data.cas90.C990000 * m_factor
    m40 = data.cas40.C400000 / data.cas90.C990000 * m_factor
    m50 = data.cas50.C500000 / data.cas90.C990000 * m_factor
    m60 = data.cas60.C600000 / data.cas90.C990000 * m_factor
    m99 = m_factor + m30 + m40 + m50 + m60

    # LIFE Values Anklam 2011
    # TODO this a_power is different than inputs.financial.a_power, are they supposed to be different?
    a_power = 1217  # this is the net electric power used because Anklan uses $/kWe

    life_values = {
        'M100000': 0,
        'M200000': m_factor,
        'M210000': (700 * a_power * 1000) / 1e6,
        'M220000': 2662 / inflation_factor,  # TODO is this correct
        'M220103': (1350 * a_power * 1000) / 1e6,
        'M2204': (170 * a_power * 1000) / (2 * 1e6),
        'M2205': (170 * a_power * 1000) / (2 * 1e6),
        'M2207': (100 * a_power * 1000) / 1e6,
        'M23': (480 * a_power * 1000) / 1e6,
        'M30': m30,
        'M40': m40,
        'M50': m50,
        'M60': m60,
        'M99': m99,
    }
    life_values_inflation = get_cost_values_inflation(life_values, inflation_factor, 2)
    life_values_percentages = get_percentage_cost_values(life_values, m99, 2)

    life_values_empty = {
        'M220100': '-',
        'M220101': '-',
        'M220102': '-',
        'M220104': '-',
        'M220105': '-',
        'M220106': '-',
        'M220107': '-',
        'M220108': '-',
        'M220109': '-',
        'M220111': '-',
        'M220119': '-',
        'M2202': '-',
        'M2203': '-',
        'M2206': '-',
        'M24': '-',
        'M25': '-',
        'M26': '-',
        'M27': '-',
        'M28': '-',
        'M29': '-',
    }
    life_values_empty_percentages = map_keys_to_percentage(life_values_empty)

    OUT.template_file = 'CASstructure.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = (rounded_cost_values | percentage_cost_values
                        | life_values_inflation | life_values_percentages
                        | life_values_empty | life_values_empty_percentages)
    return [OUT]