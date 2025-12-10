from typing import Union

from pyfecons.units import M_USD, MW, USD, W

# Unit conversions


def to_m_usd(dollars: Union[float, USD]) -> M_USD:
    return M_USD(dollars / 1e6)


def m_to_usd(dollars: Union[float, M_USD]) -> USD:
    return USD(dollars * 1e6)


# cost thousands to millions USD
def k_to_m_usd(thousands_dollars: Union[float, USD]) -> M_USD:
    return M_USD(thousands_dollars / 1e3)


def w_to_mw(watts: Union[float, W]) -> MW:
    return MW(watts / 1e6)


# EUR to USD given rate of Oct 20, 2024
def eur_to_usd(amount_eur: float) -> float:
    return 0.920015 * amount_eur


# Inflation adjustment, all from https://www.usinflationcalculator.com/
inflation_1992_2024 = 2.26
inflation_2005_2024 = 1.58
inflation_2010_2024 = 1.43
inflation_factor_2019_2024 = 1.22
