from pyfecons.data import Data


def get_cost_values(data: Data) -> dict[str, float]:
    return {
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
        'C220500': data.cas2205.C220500,
        'C220600': data.cas2206.C220600,
        'C220700': data.cas2207.C220700,
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


def get_rounded(values: dict[str, float], round_digits: int) -> dict[str, str]:
    return {key: str(round(val, round_digits)) for key, val in values.items()}


def get_percentage_cost_values(cost_values: dict[str, float], total: float, round_digits: int) -> dict[str, str]:
    return {to_percentage(key): str(round(val / total * 100, round_digits)) for key, val in cost_values.items()}


def map_keys_to_percentage(values: dict[str, str]) -> dict[str, str]:
    return {to_percentage(key): val for key, val in values.items()}


def to_percentage(key: str) -> str:
    return key[0] + '.' + key[1:] + 'pp'


def get_cost_values_inflation(values: dict[str, float], inflation_factor: float, round_digits: int):
    return {key: str(round(val * inflation_factor, round_digits)) for key, val in values.items()}
