from dataclasses import dataclass

from pyfecons.units import Ratio


@dataclass
class Shield:
    # fractions
    f_SiC: Ratio = None
    FPCPPFbLi: Ratio = None
    f_W: Ratio = None
    f_BFS: Ratio = None
