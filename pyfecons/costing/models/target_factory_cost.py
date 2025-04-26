from dataclasses import dataclass
from typing import Optional

from pyfecons.helpers import safe_round
from pyfecons.units import Ratio


@dataclass
class CostField:
    cost: Optional[float]
    scaling_factor: Optional[Ratio] = None

    @property
    def scaled_cost(self) -> Optional[float]:
        if self.cost is None or self.scaling_factor is None:
            return self.cost
        else:
            return self.cost * self.scaling_factor


@dataclass
class TargetFactoryCost:
    no_machines: CostField
    floorspace_sqrft: CostField
    wip_parts: CostField
    tcc_dollars: CostField
    annualized_cc_dollars_per_year: CostField
    consumables_electricity_maint: CostField
    personnel_costs_dollars_per_year: CostField
    cost_per_target: CostField

    @property
    def cost_row(self) -> str:
        return " & ".join(
            [
                f"{safe_round(self.no_machines.scaled_cost, 1)}",
                f"{safe_round(self.floorspace_sqrft.scaled_cost, 1)}",
                f"{safe_round(self.wip_parts.scaled_cost, 1)}",
                f"{safe_round(self.tcc_dollars.scaled_cost, 1)}",
                f"{safe_round(self.annualized_cc_dollars_per_year.scaled_cost, 1)}",
                f"{safe_round(self.consumables_electricity_maint.scaled_cost, 1)}",
                f"{safe_round(self.personnel_costs_dollars_per_year.scaled_cost, 1)}",
                f"{safe_round(self.cost_per_target.scaled_cost, 1)}",
            ]
        )
