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
    TUNGSTEN = 'tungsten'
    LIQUID_METAL = 'liquid metal'
    BERYLLIUM = 'beryllium'
    MOLTEN_SALT = 'molten salt'


class BlanketType(Enum):
    FLOWING_LIQUID_FIRST_WALL = 'Flowing liquid first wall'
    SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER = 'Solid first wall with a liquid breeder'
    SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI4SIO4 = 'Solid first wall with a solid breeder (Li4SiO4)'
    SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3 = 'Solid first wall with a solid breeder (Li2TiO3)'
    SOLID_FIRST_WALL_NO_BREEDER_ANUETRONIC_FUEL = 'Solid first wall, no breeder (anuetronic fuel)'


class BlanketPrimaryCoolant(Enum):
    LEAD_LITHIUM_PBLI = 'Lead Lithium (PbLi)'
    LITHIUM_LI = 'Lithium (Li)'
    FLIBE = 'FLiBe'
    OTHER_EUTECTIC_SALT = 'Other eutectic salt'
    HELIUM = 'Helium'
    DUAL_COOLANT_PBLI_AND_HE = 'Dual coolant: PbLi and He'
    WATER = 'Water'


class BlanketSecondaryCoolant(Enum):
    NONE = 'None'
    LEAD_LITHIUM_PBLI = 'Lead Lithium (PbLi)'
    LITHIUM_LI = 'Lithium (Li)'
    FLIBE = 'FLiBe'
    OTHER_EUTECTIC_SALT = 'Other eutectic salt'
    HELIUM = 'Helium'
    DUAL_COOLANT_PBLI_AND_HE = 'Dual coolant: PbLi and He'
    WATER = 'Water'


class BlanketNeutronMultiplier(Enum):
    NONE = 'None'
    BE = 'Be'
    PB = 'Pb'
    PB_AS_PART_OF_PBLI = 'Pb as part of PbLi'
    BE12TI = 'Be12Ti'


class BlanketStructure(Enum):
    STAINLESS_STEEL_SS = 'Stainless Steel (SS)'
    FERRITIC_MARTENSITIC_STEEL_FMS = 'Ferritic Martensitic Steel (FMS)'
    OXIDE_DISPERSION_STRENGTHENED_ODS_STEEL = 'Oxide Dispersion Strengthened (ODS) Steel'
    VANADIUM = 'Vanadium'


# PGA stands for peak ground acceleration and increasing values would correlate to an increased risk region.
class StructurePga(Enum):
    PGA_01 = 0.1
    PGA_02 = 0.2
    PGA_03 = 0.3
    PGA_05 = 0.5
