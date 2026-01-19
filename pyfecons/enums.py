from enum import Enum


class FusionMachineType(Enum):
    IFE = "IFE"
    MFE = "MFE"
    MIF = "MIF"


class ConfinementType(Enum):
    # STELLARATOR = (FusionMachineType.MFE, 'STELLARATOR')
    SPHERICAL_TOKAMAK = (FusionMachineType.MFE, "SPHERICAL_TOKAMAK")
    # CONVENTIONAL_TOKAMAK = (FusionMachineType.MFE, 'CONVENTIONAL_TOKAMAK')
    # COMPACT_TOKAMAK = (FusionMachineType.MFE, 'COMPACT_TOKAMAK')
    MAGNETIC_MIRROR = (FusionMachineType.MFE, "MAGNETIC_MIRROR")
    # SPHEROMAK = (FusionMachineType.MFE, 'SPHEROMAK')
    # RFP = (FusionMachineType.MFE, 'RFP')
    # FRC = (FusionMachineType.MFE, 'FRC')
    # MAG_LIF = (FusionMachineType.MIF, 'MAG_LIF')
    # Z_PINCH = (FusionMachineType.MIF, 'Z_PINCH')
    # PLASMA_JET = (FusionMachineType.MIF, 'PLASMA_JET')
    # MIRROR_MIF = (FusionMachineType.MIF, 'MIRROR_MIF')
    # THETA_PINCH = (FusionMachineType.MIF, 'THETA_PINCH')
    LASER_DRIVEN_DIRECT_DRIVE = (FusionMachineType.IFE, "LASER_DRIVEN_DIRECT_DRIVE")
    # LASER_DRIVEN_INDIRECT_DRIVE = (FusionMachineType.IFE, 'LASER_DRIVEN_INDIRECT_DRIVE')
    # FAST_IGNITION = (FusionMachineType.IFE, 'FAST_IGNITION')
    # IEC = (FusionMachineType.IFE, 'IEC')
    # PROJECTILE = (FusionMachineType.IFE, 'PROJECTILE')

    def __new__(cls, fusion_machine_type: FusionMachineType, value):
        obj = object.__new__(cls)
        obj.fusion_machine_type = fusion_machine_type
        obj._value_ = value
        return obj


class EnergyConversion(Enum):
    DIRECT = "DIRECT"
    TURBINE = "TURBINE"
    # HYBRID = 'HYBRID'


class FuelType(Enum):
    DT = ("DT", "Deuterium Tritium")
    DD = ("DD", "Deuterium Deuterium")
    DHE3 = ("DHE3", "Deuterium Helium-3")
    PB11 = ("PB11", "Lead Boron-11")

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj


class BlanketFirstWall(Enum):
    TUNGSTEN = ("TUNGSTEN", "Tungsten")
    LIQUID_LITHIUM = ("LIQUID_LITHIUM", "Liquid Lithium")
    BERYLLIUM = ("BERYLLIUM", "Beryllium")
    FLIBE = ("FLIBE", "FLiBe")

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj


class BlanketType(Enum):
    FLOWING_LIQUID_FIRST_WALL = (
        "FLOWING_LIQUID_FIRST_WALL",
        "Flowing Liquid First Wall",
    )
    SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER = (
        "SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER",
        "Solid First Wall with a Liquid Breeder",
    )
    SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI4SIO4 = (
        "SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI4SIO4",
        "Solid First Wall with Solid Breeder (Li4SiO4)",
    )
    SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3 = (
        "SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3",
        "Solid First Wall with Solid Breeder (Li2TiO3)",
    )
    SOLID_FIRST_WALL_NO_BREEDER_ANEUTRONIC_FUEL = (
        "SOLID_FIRST_WALL_NO_BREEDER_ANEUTRONIC_FUEL",
        "Solid First Wall No Breeder (Aneutronic Fuel)",
    )

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj


class BlanketPrimaryCoolant(Enum):
    LEAD_LITHIUM_PBLI = ("LEAD_LITHIUM_PBLI", "Lead Lithium (PbLi)")
    LITHIUM_LI = ("LITHIUM_LI", "Lithium (Li)")
    FLIBE = ("FLIBE", "FliBe")
    OTHER_EUTECTIC_SALT = ("OTHER_EUTECTIC_SALT", "Other Eutectic Salt")
    HELIUM = ("HELIUM", "Helium (He)")
    DUAL_COOLANT_PBLI_AND_HE = ("DUAL_COOLANT_PBLI_AND_HE", "Dual Coolant: PbLi and He")
    WATER = ("WATER", "Water")

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj


class BlanketSecondaryCoolant(Enum):
    NONE = ("NONE", "None")
    LEAD_LITHIUM_PBLI = ("LEAD_LITHIUM_PBLI", "Lead Lithium (PbLi)")
    LITHIUM_LI = ("LITHIUM_LI", "Lithium (Li)")
    FLIBE = ("FLIBE", "FliBe")
    OTHER_EUTECTIC_SALT = ("OTHER_EUTECTIC_SALT", "Other Eutectic Salt")
    HELIUM = ("HELIUM", "Helium (He)")
    DUAL_COOLANT_PBLI_AND_HE = ("DUAL_COOLANT_PBLI_AND_HE", "Dual Coolant: PbLi and He")
    WATER = ("WATER", "Water")

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj


class BlanketNeutronMultiplier(Enum):
    NONE = ("NONE", "None")
    BE = ("BE", "Beryllium (Be)")
    PB = ("PB", "Lead (Pb)")
    PB_AS_PART_OF_PBLI = ("PB_AS_PART_OF_PBLI", "Pb as part of PbLi")
    BE12TI = ("BE12TI", "Beryllium Titanium (Be12Ti)")

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj


class BlanketStructure(Enum):
    STAINLESS_STEEL_SS = ("STAINLESS_STEEL_SS", "Stainless Steel (SS)")
    FERRITIC_MARTENSITIC_STEEL_FMS = (
        "FERRITIC_MARTENSITIC_STEEL_FMS",
        "Ferritic Martensitic Steel (FMS)",
    )
    OXIDE_DISPERSION_STRENGTHENED_ODS_STEEL = (
        "OXIDE_DISPERSION_STRENGTHENED_ODS_STEEL",
        "Oxide Dispersion Strengthened Steel (ODS)",
    )
    VANADIUM = ("VANADIUM", "Vanadium")

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj


# PGA stands for peak ground acceleration and increasing values would correlate to an increased risk region.
class StructurePga(Enum):
    PGA_01 = 0.1
    PGA_02 = 0.2
    PGA_03 = 0.3
    PGA_05 = 0.5


class MagnetType(Enum):
    PF = ("PF", "Poloidal Field")
    CS = ("CS", "Central Solonoid")
    TF = ("TF", "Toroidal Field")

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj


class MagnetMaterialType(Enum):
    HTS_CICC = ("HTS_CICC", "HTS CICC")
    HTS_PANCAKE = ("HTS_PANCAKE", "HTS Pancake")
    COPPER = ("COPPER", "Copper")

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj


class Region(Enum):
    US = ("US", "United States")
    UK = ("UK", "United Kingdom")
    UNSPECIFIED = ("UNSPECIFIED", "Unspecified")

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj
