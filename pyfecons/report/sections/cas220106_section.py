from dataclasses import dataclass

from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.costing.categories.cas220106 import CAS220106
from pyfecons.enums import FusionMachineType
from pyfecons.inputs.vacuum_system import VacuumSystem
from pyfecons.report.section import ReportSection


@dataclass
class CAS220106Section(ReportSection):
    def __init__(
        self,
        cas220106: CAS220106,
        fusion_machine_type: FusionMachineType,
        vacuum_system: VacuumSystem,
    ):
        super().__init__()

        self.cas220106 = cas220106
        if fusion_machine_type == FusionMachineType.MFE:
            self._init_mfe(cas220106)
        elif fusion_machine_type == FusionMachineType.IFE:
            self._init_ife(cas220106, vacuum_system)
        else:
            raise ValueError(f"Unsupported reactor type: {fusion_machine_type}")

    def _init_mfe(self, cas220106: CAS220106):
        self.template_file = "CAS220106_MFE.tex"
        self.replacements = {
            "C22010601": round(cas220106.C22010601),
            "C22010602": round(cas220106.C22010601),
            "C22010603": round(cas220106.C22010603),
            "C22010604": round(cas220106.C22010604),
            "C22010600": round(cas220106.C220106),
            "vesvol": round(cas220106.ves_vol),
            "massstruct": round(cas220106.mass_struct),
            "vesmatcost": round(
                to_m_usd(cas220106.vessel_costs.total.material_cost), 1
            ),
        }

    def _init_ife(self, cas220106: CAS220106, vacuum_system: VacuumSystem):
        self.template_file = "CAS220106_IFE.tex"
        self.replacements = {
            "C22010601": round(cas220106.C22010601),
            "C22010602": round(cas220106.C22010602),
            "C22010603": round(cas220106.C22010603),
            "C22010604": round(cas220106.C22010604, 2),
            "C22010600": round(cas220106.C220106),
            "vesvol": round(cas220106.ves_vol),
            "materialvolume": round(cas220106.material_volume),
            "massstruct": round(cas220106.mass_struct / 1e3),
            "vesmatcost": round(to_m_usd(cas220106.ves_mat_cost), 1),
            "vesmfr": round(vacuum_system.ves_mfr),
        }
