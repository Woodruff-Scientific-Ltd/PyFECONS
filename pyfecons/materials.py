from dataclasses import dataclass

from pyfecons.units import KG_M3, USD_M3, USD_KG, Megapascal


@dataclass
class Material:
    name: str = None
    abbr: str = None
    rho: KG_M3 = None  # Density
    c: USD_M3 = None  # Cost per unit volume
    c_raw: USD_KG = None  # Cost per unit mass
    m: float = None  # Mass factor or multiplier (unitless) - TODO clarify this unit
    sigma: Megapascal = None


# TODO what is this constant and where does it come from?
_pblir = 10

def _pbli_rho(pb: Material, li: Material) -> KG_M3:
    return KG_M3((pb.rho * _pblir + li.rho) / (_pblir + 1))


def _pbli_c(pb: Material, li: Material) -> USD_M3:
    return USD_M3((pb.c_raw * pb.m * _pblir + li.c_raw * li.m) / (_pblir + 1))


class Materials:
    # TODO figure out what material FS is supposed to represent. GPT suggests HT9.
    FERRITIC_STEEL = Material(name="Ferritic Steel", abbr='FS', rho=7470, c_raw=10, m=3, sigma=450)
    LEAD = Material(name="Lead", abbr='Pb', rho=9400, c_raw=2.4, m=1.5)
    LITHIUM_SILICATE = Material(name="Lithium Silicate", abbr='Li4SiO4', rho=2390, c_raw=1, m=2)
    # TODO figure out actual value c_raw and m for FliBe, these are currently placeholders
    FLIBE = Material(name="Lithium Fluoride (LiF) and Beryllium Fluoride (BeF2) Mixture", abbr='FliBe', rho=1900, c=40, c_raw=1000, m=1)
    TUNGSTEN = Material(name="Tungsten", abbr='W', rho=19300, c_raw=100, m=3)
    LITHIUM = Material(name="Lithium", abbr='Li', rho=534, c_raw=70, m=1.5)
    BFS = Material(name="BFS", abbr='BFS', rho=7800, c_raw=30, m=2)
    SILICON_CARBIDE = Material(name="Silicon Carbide", abbr='SiC', rho=3200, c_raw=14.49, m=3)
    INCONEL = Material(name="Inconel", abbr='Inconel', rho=8440, c_raw=46, m=3)
    COPPER = Material(name="Copper", abbr='Cu', rho=7300, c_raw=10.2, m=3)
    POLYIMIDE = Material(name="Polyimide", abbr='Polyimide', rho=1430, c_raw=100, m=3)
    YBCO = Material(name="Yttrium Barium Copper Oxide (YBa2Cu3O7)", abbr='YBCO', rho=6200, c=55)
    CONCRETE = Material(name="Concrete", abbr='Concrete', rho=2300, c_raw=13/25, m=2)
    STAINLESS_STEEL_SS316 = Material(name="Stainless Steel 316", abbr='SS316', rho=7860, c_raw=2, m=2, sigma=900)
    NB3SN = Material(name="Niobium-Tin", abbr='Nb3Sn', c=5)
    INCOLOY = Material(name="Incoloy", abbr='Incoloy', rho=8170, c_raw=4, m=2)
    GDBCO = Material(name="Gadolinium Barium Copper Oxide", abbr='GdBCO')  # Density and cost not provided
    HELIUM = Material(name="Helium", abbr='He')  # Density and cost not provided
    NBTI = Material(name="Niobium-Titanium", abbr='NbTi')  # Density and cost not provided
    BERYLLIUM = Material(name="Beryllium", abbr='Be', rho=1850, c_raw=5750, m=3)
    LITHIUM_TITANATE = Material(name="Lithium Titanate", abbr='Li2TiO3', rho=3430, c_raw=1297.05, m=3)
    PBLI = Material(name="Lead (Pb) and Lithium (Li) Eutectic Alloy", abbr='PbLi', rho=_pbli_rho(LEAD, LITHIUM), c=_pbli_c(LEAD, LITHIUM))
    HT9 = Material(name="Modified 9Cr-1Mo Ferritic-Martensitic Steel", abbr='HT9', rho=7800)
    MA957 = Material(name="Mechanically Alloyed 14% Chromium Oxide Dispersion Strengthened Ferritic-Martensitic Steel", abbr='MA957', rho=7600)
    VANADIUM_ALLOY = Material(name="Vanadium Alloy", abbr='V-15Cr-5Ti', rho=6100)
    TZM = Material(name='Titanium-Zirconium-Molybdenum', abbr='TZM', rho=10200)
