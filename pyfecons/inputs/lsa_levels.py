from dataclasses import dataclass


@dataclass
class LsaLevels:
    lsa: int
    initialized: bool = False
    fac_91: list[float] = None
    fac_92: list[float] = None
    fac_93: list[float] = None
    fac_94: list[float] = None
    fac_95: list[float] = None
    fac_96: list[float] = None
    fac_97: list[float] = None
    fac_98: list[float] = None

    def __post_init__(self):
        if not self.initialized:
            # Indirect Cost Factors for different LSA levels
            self.fac_91 = [0.1130, 0.1200, 0.1280, 0.1510]  # x TDC [90]
            self.fac_92 = [0.0520, 0.0520, 0.0520, 0.0520]  # x TDC [90]
            self.fac_93 = [0.0520, 0.0600, 0.0640, 0.0870]  # x TDC [90]
            self.fac_94 = [
                0.1826,
                0.1848,
                0.1866,
                0.1935,
            ]  # applies only to C90, x TDC [90+91+92+93]
            self.fac_95 = [0.0000, 0.0000, 0.0000, 0.0000]  # x TDC [90+91+92+93+94]
            self.fac_96 = [
                0.2050,
                0.2391,
                0.2565,
                0.2808,
            ]  # applied only to C90, x TDC [90+91+92+93+94]
            self.fac_97 = [
                0.2651,
                0.2736,
                0.2787,
                0.2915,
            ]  # applied only to C90, x TDC [90+91+92+93+94+95+96]
            self.fac_98 = [
                0.0000,
                0.0000,
                0.0000,
                0.0000,
            ]  # x TDC [90+91+92+93+94+95+96]
            self.initialized = True
