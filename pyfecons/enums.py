from enum import Enum


class ReactorType(Enum):
    LASER = 'LASER'
    MIRROR = 'MIRROR'
    STELLARATOR = 'STELLARATOR'
    TOKAMAK = 'TOKAMAK'


class EnergyConversion(Enum):
    DIRECT = 'DIRECT'
    TURBINE = 'TURBINE'


class FuelType(Enum):
    DT = 'DT'
    DHE3 = 'DHE3'
    PB11 = 'PB11'
