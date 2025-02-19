from dataclasses import dataclass

from pyfecons.units import M_USD


# 22.1.5 primary structure
@dataclass
class PgaCosts:
    eng_costs: M_USD
    fab_costs: M_USD
