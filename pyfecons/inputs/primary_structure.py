from dataclasses import dataclass

from pyfecons.enums import StructurePga
from pyfecons.inputs.pga_costs import PgaCosts
from pyfecons.units import Ratio, M_USD


@dataclass
class PrimaryStructure:
    # PGA stands for peak ground acceleration and increasing values would correlate to an increased risk region.
    syst_pga: StructurePga = None
    learning_credit: Ratio = None
    # percentage of components replaced over the plant lifetime
    replacement_factor: Ratio = None

    analyze_costs: M_USD = 30
    unit1_seismic_costs: M_USD = 25
    reg_rev_costs: M_USD = 30
    unit1_fab_costs: M_USD = 100
    unit10_fabcosts: M_USD = 70
    pga_costs_mapping: dict[str, PgaCosts] = None

    # Dictionary of fission reactor costs from "Towards standardized nuclear reactors: Seismic isolation and the cost
    # impact of the earthquake load case" URL: https://www.sciencedirect.com/science/article/abs/pii/S0029549321004398

    def __post_init__(self):
        if self.pga_costs_mapping is None:
            self.pga_costs_mapping = {
                StructurePga.PGA_01.name: PgaCosts(
                    eng_costs=M_USD(115), fab_costs=M_USD(115)
                ),
                StructurePga.PGA_02.name: PgaCosts(
                    eng_costs=M_USD(125), fab_costs=M_USD(130)
                ),
                StructurePga.PGA_03.name: PgaCosts(
                    eng_costs=M_USD(140), fab_costs=M_USD(165)
                ),
                StructurePga.PGA_05.name: PgaCosts(
                    eng_costs=M_USD(160), fab_costs=M_USD(235)
                ),
            }

    def get_pga_costs(self) -> PgaCosts:
        return self.pga_costs_mapping[self.syst_pga.name]
