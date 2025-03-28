class Years(float):
    pass


class Amperes(float):
    def __str__(self):
        return f"{self:.2f}"


class MA(float):
    def __str__(self):
        return f"{self:.2f}"


# Watts
class W(float):
    def __str__(self):
        return f"{self:.2f}"


# Megawatts
class MW(float):
    def __str__(self):
        return f"{self:.2f}"


# A/mm$^2$
class AmperesMillimeters2(float):
    def __str__(self):
        return f"{self:.2f}"


class Kilograms(float):
    def __str__(self):
        return f"{self:.2f}"


class Meters(float):
    def __str__(self):
        return f"{self:.2f}"


class Kilometers(float):
    def __str__(self):
        return f"{self:.2f}"


# area
class Meters2(float):
    def __str__(self):
        return f"{self:.2f}"


# volume
class Meters3(float):
    def __str__(self):
        return f"{self:.2f}"


# Dimensionless
class Count(int):
    pass


# Dimensionless
class Percent(float):
    def __str__(self):
        return f"{self:.2f}"


# Dimensionless
class Ratio(float):
    def __str__(self):
        return f"{self:.3f}"


class USD(float):
    def __str__(self):
        return f"{self:.2f}"


# Was Currency, renamed to M_USD
# The templates suggest this is in millions of USD
class M_USD(float):
    def __str__(self):
        return f"{self:.2f}"


# technically unitless
class Turns(float):
    def __str__(self):
        return f"{self:.2f}"


class Unknown(float):
    def __str__(self):
        return f"{self:.2f}"


# Hertz
class HZ(float):
    def __str__(self):
        return f"{self:.2f}"


# Megajoules
class MJ(float):
    def __str__(self):
        return f"{self:.2f}"


# Temperature Kelvin
class K(float):
    def __str__(self):
        return f"{self:.2f}"


# USD per W
class USD_W(float):
    def __str__(self):
        return f"{self:.2f}"


# Voltage
class V(float):
    def __str__(self):
        return f"{self:.2f}"


# Density - kg/m^3
class KG_M3(float):
    def __str__(self):
        return f"{self:.2f}"


# Cost per unit volume - USD/m^3
class USD_M3(float):
    def __str__(self):
        return f"{self:.2f}"


# Cost per unit mass - USD/kg
class USD_KG(float):
    def __str__(self):
        return f"{self:.2f}"


# unit of pressure or stress - N/m^2
class Megapascal(float):
    def __str__(self):
        return f"{self:.2f}"
