from dataclasses import dataclass

from pyfecons.units import KG_M3, USD_M3, USD_KG, Megapascal


@dataclass
class Material:
    name: str = None
    rho: KG_M3 = None  # Density
    c: USD_M3 = None  # Cost per unit volume
    c_raw: USD_KG = None  # Cost per unit mass
    m: float = None  # Mass factor or multiplier (unitless) - TODO clarify this unit
    sigma: Megapascal = None


class Materials:
    def __init__(self):
        self.FS = Material(name="Ferritic Steel", rho=7470, c_raw=10, m=3, sigma=450)
        self.Pb = Material(name="Lead", rho=9400, c_raw=2.4, m=1.5)
        self.Li4SiO4 = Material(name="Lithium Silicate", rho=2390, c_raw=1, m=2)
        # TODO figure out actual value c_raw and m for FliBe, these are currently placeholders
        self.FliBe = Material(
            name="Lithium Fluoride (LiF) and Beryllium Fluoride (BeF2) Mixture",
            rho=1900,
            c=40,
            c_raw=1000,
            m=1,
        )
        self.W = Material(name="Tungsten", rho=19300, c_raw=100, m=3)
        self.Li = Material(name="Lithium", rho=534, c_raw=70, m=1.5)
        self.BFS = Material(name="BFS", rho=7800, c_raw=30, m=2)
        self.SiC = Material(name="Silicon Carbide", rho=3200, c_raw=14.49, m=3)
        self.Inconel = Material(name="Inconel", rho=8440, c_raw=46, m=3)
        self.Cu = Material(name="Copper", rho=7300, c_raw=10.2, m=3)
        self.Polyimide = Material(name="Polyimide", rho=1430, c_raw=100, m=3)
        self.YBCO = Material(
            name="Yttrium Barium Copper Oxide (YBa2Cu3O7)", rho=6200, c=55
        )
        self.Concrete = Material(name="Concrete", rho=2300, c_raw=13 / 25, m=2)
        self.SS316 = Material(
            name="Stainless Steel 316", rho=7860, c_raw=2, m=2, sigma=900
        )
        self.Nb3Sn = Material(name="Niobium-Tin (Nb3Sn)", c=5)
        self.Incoloy = Material(name="Incoloy", rho=8170, c_raw=4, m=2)
        self.GdBCO = Material(
            name="Gadolinium Barium Copper Oxide"
        )  # Density and cost not provided
        self.He = Material(name="Helium")  # Density and cost not provided
        self.NbTi = Material(name="Niobium-Titanium")  # Density and cost not provided
        self.Be = Material(name="Beryllium", rho=1850, c_raw=5750, m=3)
        self.Li2TiO3 = Material(name="Lithium Titanate", rho=3430, c_raw=1297.05, m=3)

        # Values to be calculated
        pblir = 10
        pbli_rho = (self.Pb.rho * pblir + self.Li.rho) / (pblir + 1)
        pbli_c = (self.Pb.c_raw * self.Pb.m * pblir + self.Li.c_raw * self.Li.m) / (
            pblir + 1
        )
        self.PbLi = Material(
            name="Lead (Pb) and Lithium (Li) Eutectic Alloy", rho=pbli_rho, c=pbli_c
        )
