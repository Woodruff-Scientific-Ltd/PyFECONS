from enum import Enum


class ReactorType(Enum):
    IFE = 'IFE'
    MFE = 'MFE'
    MIF = 'MIF'


class EnergyConversion(Enum):
    DIRECT = 'DIRECT'
    TURBINE = 'TURBINE'


class FuelType(Enum):
    DT = 'DT' # for now only one type of fuel
    # DHE3 = 'DHE3'
    # PB11 = 'PB11'
