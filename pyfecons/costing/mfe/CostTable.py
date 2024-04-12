from pyfecons.inputs import Inputs
from pyfecons.data import Data

CAS_STRUCTURE_TEX = 'CASstructure.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    cost_values = {
        'C100000': data.cas10.C100000,
        'C200000': data.cas20.C200000,
        'C210000': data.cas21.C210000,
        'C220000': data.cas22.C220000,
        'C220100': data.cas22.C220100,
        'C220101': data.cas220101.C220101,
        'C220102': data.cas220102.C220102,
        'C220103': data.cas220103.C220103,
        'C220104': data.cas220104.C220104,
        'C220105': data.cas220105.C220105,
        'C220106': data.cas220106.C220106,
        'C220107': data.cas220107.C220107,
        'C220108': data.cas220108.C220108,
        'C220109': data.cas220109.C220109,
        'C220111': data.cas220111.C220111,
        'C220119': data.cas220119.C220119,
        'C220200': data.cas2202.C220200,
        'C220300': data.cas2203.C220300,
        'C220400': data.cas2204.C220400,
        'C220500': data.cas22.C220500,
        'C220600': data.cas22.C220600,
        'C220700': data.cas22.C220700,
        'C230000': data.cas23.C230000,
        'C240000': data.cas24.C240000,
        'C250000': data.cas25.C250000,
        'C260000': data.cas26.C260000,
        'C270000': data.cas27.C270000,
        'C280000': data.cas28.C280000,
        'C290000': data.cas29.C290000,
        'C300000': data.cas30.C300000,
        'C400000': data.cas40.C400000,
        'C500000': data.cas50.C500000,
        'C600000': data.cas60.C600000,
        'C990000': data.cas90.C990000,
    }
    rounded_cost_values = {key: str(round(val, 2)) for key, val in cost_values.items()}
    percentage_cost_values = {percentage(key): str(round(val / data.cas90.C990000 * 100, 2)) for key, val in cost_values.items()}

    # ARIES ST
    inflation_factor = 1.35
    # TODO - what is 4479.7?
    m30 = data.cas30.C300000/data.cas90.C990000*4479.7
    m40 = data.cas40.C400000/data.cas90.C990000*4479.7
    m50 = data.cas50.C500000/data.cas90.C990000*4479.7
    m60 = data.cas60.C600000/data.cas90.C990000*4479.7
    m99 = 4479.7+m30+m40+m50+m60
    a_power = 2920  # this is the net electric power - TODO this is not used

    aries_st_values = {
        'M100000': 10.6,
        'M200000': 4479.7,
        'M210000': 370.8,
        'M220000': 1244.1,
        'M220100': 648.7,
        'M220101': 50.2,
        'M220102': 113.1,
        'M220103': 102.6,
        'M220104': 212.5,
        'M220105': 37.4,
        'M220106': 48.1,
        'M220107': 71.6,
        'M220108': 8.8,
        'M220119': 358,
        'M2207': 3.49,
        'M23': 339,
        'M24': 125.4,
        'M25': 77.9,
        'M26': 64.3,
        'M27': 108.9,
        'M29': 555.1,
        'M30': m30,
        'M40': 429,
        'M50': m50,
        'M60': m60,
        'M99': m99,
    }

    aries_st_empty_values = {
        'M220109': '-',
        'M220111': '-',
        'M2202': '-',
        'M2203': '-',
        'M2204': '-',
        'M2205': '-',
        'M2206': '-',
        'M28': '-',
    }

    aries_st_values_inflation = {key: str(round(val*inflation_factor, 2)) for key, val in aries_st_values.items()}
    aries_st_percentages = {percentage(key): str(round(val / m99 * 100, 2)) for key, val in aries_st_values.items()}
    aries_st_empty_percentages = {percentage(key): val for key, val in aries_st_empty_values.items()}

    data.cost_table.template_file = CAS_STRUCTURE_TEX
    data.cost_table.replacements = (rounded_cost_values | percentage_cost_values
                                    | aries_st_values_inflation | aries_st_percentages
                                    | aries_st_empty_values | aries_st_empty_percentages)


def percentage(key):
    return key[0] + '.' + key[1:] + 'pp'
