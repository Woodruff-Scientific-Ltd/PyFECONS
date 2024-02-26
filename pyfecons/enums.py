from enum import Enum


class ReactorType(Enum):
    IFE = 'IFE'
    MFE = 'MFE'
    MIF = 'MIF'


class EnergyConversion(Enum):
    DIRECT = 'DIRECT'
    TURBINE = 'TURBINE'


class FuelType(Enum):
    DT = 'DT'  # for now only one type of fuel
    # DHE3 = 'DHE3'
    # PB11 = 'PB11'


class BlanketFirstWall(Enum):
    TUNGSTEN = 'TUNGSTEN'
    LIQUID_METAL = 'LIQUID_METAL'
    BERYLLIUM = 'BERYLLIUM'
    MOLTEN_SALT = 'MOLTEN_SALT'


class BlanketType(Enum):
    FLOWING_LIQUID_FIRST_WALL = 'FLOWING_LIQUID_FIRST_WALL'
    SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER_LI4SIO4 = 'SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER_LI4SIO4'
    SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3 = 'SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3'
    SOLID_FIRST_WALL = 'SOLID_FIRST_WALL'
    NO_BREEDER_ANEUTRONIC_FUEL = 'NO_BREEDER_ANEUTRONIC_FUEL'


class BlanketPrimaryCoolant(Enum):
    LEAD_LITHIUM_PBLI = 'LEAD_LITHIUM_PBLI'
    LITHIUM_LI = 'LITHIUM_LI'
    FLIBE = 'FLIBE'


class BlanketSecondaryCoolant(Enum):
    NONE = 'NONE'
    LEAD_LITHIUM_PBLI = 'LEAD_LITHIUM_PBLI'
    LITHIUM_LI = 'LITHIUM_LI'
    FLIBE = 'FLIBE'


class BlanketNeutronMultiplier(Enum):
    NONE = 'NONE'
    BE = 'BE'
    PB = 'PB'
    PB_AS_PART_OF_PBLI = 'PB_AS_PART_OF_PBLI'
    BE12TI = 'BE12TI'


class BlanketStructure(Enum):
    STAINLESS_STEEL_SS = 'STAINLESS_STEEL_SS'
    FERRITIC_MARTENSITIC_STEEL_FMS = 'FERRITIC_MARTENSITIC_STEEL_FMS'
    OXIDE_DISPERSION_STRENGTHENED_ODS_STEEL = 'OXIDE_DISPERSION_STRENGTHENED_ODS_STEEL'
    VANADIUM = 'VANADIUM'


# PGA stands for peak ground acceleration and increasing values would correlate to an increased risk region.
class StructurePga(Enum):
    PGA_01 = 0.1
    PGA_02 = 0.2
    PGA_03 = 0.3
    PGA_05 = 0.5
