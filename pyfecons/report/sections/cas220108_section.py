from dataclasses import dataclass
from typing import Union

from pyfecons.costing.categories.cas220108_divertor import CAS220108Divertor
from pyfecons.costing.categories.cas220108_target_factory import CAS220108TargetFactory
from pyfecons.enums import FusionMachineType
from pyfecons.figures import TargetPfrFigure
from pyfecons.report.section import ReportSection


@dataclass
class CAS220108Section(ReportSection):
    def __init__(
        self,
        cas220108: Union[CAS220108Divertor, CAS220108TargetFactory],
        fusion_machine_type: FusionMachineType,
    ):
        super().__init__()
        if fusion_machine_type == FusionMachineType.MFE:
            self._init_mfe(cas220108)
        elif fusion_machine_type == FusionMachineType.IFE:
            self._init_ife(cas220108)
        else:
            raise ValueError(f"Unsupported reactor type: {fusion_machine_type}")

    def _init_mfe(self, cas220108: CAS220108Divertor):
        self.template_file = "CAS220108_MFE.tex"
        self.replacements = {
            "C220108": round(cas220108.C220108),
            # All of these are not in the templateo
            "divertorMajRad": str(round(cas220108.divertor_maj_rad)),
            "divertorMinRad": str(round(cas220108.divertor_min_rad)),
            "divertorThicknessZ": str(round(cas220108.divertor_thickness_z)),
            "divertorMaterial": str(cas220108.divertor_material.name),
            "divertorVol": str(round(cas220108.divertor_vol)),
            "divertorMass": str(round(cas220108.divertor_mass)),
        }

    def _init_ife(self, cas220108: CAS220108TargetFactory):
        self.figures["Figures/targetPFR.pdf"] = TargetPfrFigure.create()
        self.template_file = "CAS220108_IFE.tex"
        self.replacements = {
            "C220108": str(round(cas220108.C220108)),
            "cvdDiamondAblatorCosts": cas220108.target_factory_costs[
                "CVD diamond ablator"
            ].cost_row,
            "dtFillCosts": cas220108.target_factory_costs["DT Fill"].cost_row,
            "hohlraumPressCosts": cas220108.target_factory_costs[
                "Hohlraum press"
            ].cost_row,
            "tentAssyCosts": cas220108.target_factory_costs["Tent assy"].cost_row,
            "hohlraumCapsuleAssy": cas220108.target_factory_costs[
                "Hohlraum-capsule assy"
            ].cost_row,
            "lehWindowAttach": cas220108.target_factory_costs[
                "LEH window attach"
            ].cost_row,
            "dtIceForm": cas220108.target_factory_costs["DT ice form"].cost_row,
            "recoverAndRecycle": cas220108.target_factory_costs[
                "Recover and recycle"
            ].cost_row,
            "facilityManagementCosts": cas220108.target_factory_costs[
                "Facility management costs"
            ].cost_row,
            "totalProcess": cas220108.target_factory_costs["Total process"].cost_row,
            "addMaterial": cas220108.target_factory_costs["Add material"].cost_row,
        }
