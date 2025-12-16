from dataclasses import dataclass
from typing import Union

from pyfecons.costing.categories.cas220103_coils import CAS220103Coils
from pyfecons.costing.categories.cas220103_lasers import CAS220103Lasers
from pyfecons.costing.categories.cas220104_ignition_lasers import (
    CAS220104IgnitionLasers,
)
from pyfecons.costing.categories.cas220104_supplementary_heating import (
    CAS220104SupplementaryHeating,
)
from pyfecons.costing.ife.cas22.nif_costs import NifCost
from pyfecons.enums import FusionMachineType
from pyfecons.helpers import safe_round
from pyfecons.inputs.supplementary_heating import SupplementaryHeating
from pyfecons.report.section import ReportSection


@dataclass
class CAS220104Section(ReportSection):
    def __init__(
        self,
        cas220104: Union[CAS220104SupplementaryHeating, CAS220104IgnitionLasers],
        fusion_machine_type: FusionMachineType,
        heating: SupplementaryHeating = None,
        cas220103: Union[CAS220103Coils, CAS220103Lasers] = None,
    ):
        super().__init__()

        self.cas220104 = cas220104
        if fusion_machine_type == FusionMachineType.MFE:
            self._init_mfe_supplementary_heating(cas220104, heating)
        elif fusion_machine_type == FusionMachineType.IFE:
            self._init_ife_ignition_lasers(cas220104, cas220103)
        else:
            raise ValueError(f"Unsupported reactor type: {fusion_machine_type}")

    def _init_mfe_supplementary_heating(
        self, cas220104: CAS220104SupplementaryHeating, heating: SupplementaryHeating
    ):
        self.template_file = "CAS220104_MFE_DT.tex"

        heating_table_rows = "\n".join(
            [
                f"        {ref.name} & {ref.type} & {round(ref.power, 2)} "
                + f"& {safe_round(ref.cost_2009, 2)} & {round(ref.cost_2023, 2)} \\\\"
                for ref in heating.heating_refs()
            ]
        )

        self.replacements = {
            "C22010401": str(round(cas220104.C22010401, 3)),
            "C22010402": str(round(cas220104.C22010402, 3)),
            "C220104__": str(round(cas220104.C220104, 3)),
            "NBIPOWER": str(round(heating.nbi_power, 3)),
            "ICRFPOWER": str(round(heating.icrf_power, 3)),
            "HEATING_TABLE_ROWS": heating_table_rows,
        }

    def _init_ife_ignition_lasers(
        self, cas220104: CAS220104IgnitionLasers, cas220103: CAS220103Lasers
    ):
        """Initialize for IFE case."""
        replacements = get_nif_replacements(cas220104.scaled_costs)
        replacements["C220103"] = str(round(cas220103.C220103))
        replacements["C220104XX"] = str(round(cas220104.C220104))
        # TODO missing value for C22010402 in template

        self.template_file = "CAS220104_IFE_DT.tex"
        self.replacements = replacements


def get_nif_replacements(scaled_costs: dict[str, NifCost]) -> dict[str, str]:
    replacements = {}
    for nif_cost in scaled_costs.values():
        replacements[nif_cost.base_key + "Procurement"] = str(
            round(nif_cost.procurement, 1)
        )
        replacements[nif_cost.base_key + "Design"] = str(round(nif_cost.design, 1))
        replacements[nif_cost.base_key + "Assembly"] = str(round(nif_cost.assembly, 1))
        replacements[nif_cost.base_key + "Total"] = str(round(nif_cost.total, 1))
    return replacements
