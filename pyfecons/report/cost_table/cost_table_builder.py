from pyfecons.costing_data import CostingData


def get_cost_values(costing_data: CostingData) -> dict[str, float]:
    return {
        "C100000": costing_data.cas10.C100000,
        "C200000": costing_data.cas20.C200000,
        "C210000": costing_data.cas21.C210000,
        "C220000": costing_data.cas22.C220000,
        "C220100": costing_data.cas22.C220100,
        "C220101": costing_data.cas220101.C220101,
        "C220102": costing_data.cas220102.C220102,
        "C220103": costing_data.cas220103.C220103,
        "C220104": costing_data.cas220104.C220104,
        "C220105": costing_data.cas220105.C220105,
        "C220106": costing_data.cas220106.C220106,
        "C220107": costing_data.cas220107.C220107,
        "C220108": costing_data.cas220108.C220108,
        "C220109": costing_data.cas220109.C220109,
        "C220111": costing_data.cas220111.C220111,
        "C220119": costing_data.cas220119.C220119,
        "C220200": costing_data.cas2202.C220200,
        "C220300": costing_data.cas2203.C220300,
        "C220400": costing_data.cas2204.C220400,
        "C220500": costing_data.cas2205.C220500,
        "C220600": costing_data.cas2206.C220600,
        "C220700": costing_data.cas2207.C220700,
        "C230000": costing_data.cas23.C230000,
        "C240000": costing_data.cas24.C240000,
        "C250000": costing_data.cas25.C250000,
        "C260000": costing_data.cas26.C260000,
        "C270000": costing_data.cas27.C270000,
        "C280000": costing_data.cas28.C280000,
        "C290000": costing_data.cas29.C290000,
        "C300000": costing_data.cas30.C300000,
        "C400000": costing_data.cas40.C400000,
        "C500000": costing_data.cas50.C500000,
        "C600000": costing_data.cas60.C600000,
        "C990000": costing_data.cas90.C990000,
    }


def get_rounded(values: dict[str, float], round_digits: int) -> dict[str, str]:
    return {key: str(round(val, round_digits)) for key, val in values.items()}


def get_percentage_cost_values(
    cost_values: dict[str, float], total: float, round_digits: int
) -> dict[str, str]:
    return {
        to_percentage(key): str(round(val / total * 100, round_digits))
        for key, val in cost_values.items()
    }


def map_keys_to_percentage(values: dict[str, str]) -> dict[str, str]:
    return {to_percentage(key): val for key, val in values.items()}


def to_percentage(key: str) -> str:
    return key[0] + "." + key[1:] + "pp"


def get_cost_values_inflation(
    values: dict[str, float], inflation_factor: float, round_digits: int
):
    return {
        key: str(round(val * inflation_factor, round_digits))
        for key, val in values.items()
    }
