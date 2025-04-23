from dataclasses import dataclass
from typing import Dict, Union

from pyfecons.report.section import ReportSection
from pyfecons.costing.categories.cas220103_coils import CAS220103Coils
from pyfecons.costing.categories.cas220103_lasers import CAS220103Lasers
from pyfecons.enums import ReactorType
from pyfecons.inputs.lasers import Lasers
from pyfecons.inputs.power_input import PowerInput
from pyfecons.costing.ife.cas22.nif_costs import (
    get_nif_scaled_costs,
    get_nif_replacements,
)


@dataclass
class CAS220103Section(ReportSection):
    """Report section for CAS220103 (Coils or Lasers) data based on reactor type."""

    def __init__(
        self,
        cas220103: Union[CAS220103Coils, CAS220103Lasers],
        reactor_type: ReactorType,
        power_input: PowerInput = None,
        lasers: Lasers = None,
        coils=None,
    ):
        super().__init__()

        if reactor_type == ReactorType.MFE:
            if coils is None:
                raise ValueError(
                    "coils parameter must be provided for MFE reactor type"
                )
            self._init_mfe_coils(cas220103, coils)
        elif reactor_type == ReactorType.IFE:
            self._init_ife_lasers(cas220103, power_input, lasers)
        else:
            raise ValueError(f"Unsupported reactor type: {reactor_type}")

    def _init_mfe_coils(self, cas220103: CAS220103Coils, coils):
        """Initialize for MFE coils case."""
        self.template_file = "CAS220103_MFE_DT_tokamak.tex"

        # Create replacements dictionary with the same values that were in the original file
        self.replacements = {
            "C220103__": str(cas220103.C220103),
            "C22010301": str(cas220103.C22010301),
            "C22010302": str(cas220103.C22010302),
            "C22010303": str(cas220103.C22010303),
            "C22010304": str(cas220103.C22010304),
            "C22010305": str(cas220103.C22010305),
            "C22010306": str(cas220103.C22010306),
            "structFactor": str(coils.struct_factor),
            "mcostI": str(coils.m_cost_ybco),
            "nopfcoils": str(cas220103.no_pf_coils),
            "nopfpairs": str(cas220103.no_pf_pairs),
            "mCostYBCO": str(coils.m_cost_ybco),
            "tableStructure": ("l" + "c" * len(cas220103.magnet_properties)),
            "tableHeaderList": (
                " & ".join(
                    [
                        f"\\textbf{{{props.magnet.name}}}"
                        for props in cas220103.magnet_properties
                    ]
                )
            ),
            "magnetTypeList": (
                " & ".join(
                    [
                        f"\\textbf{{{props.magnet.material_type.display_name}}}"
                        for props in cas220103.magnet_properties
                    ]
                )
            ),
            "magnetRadiusList": (
                " & ".join(
                    [
                        f"{props.magnet.r_centre}"
                        for props in cas220103.magnet_properties
                    ]
                )
            ),
            "magnetDrList": (
                " & ".join(
                    [f"{props.magnet.dr}" for props in cas220103.magnet_properties]
                )
            ),
            "magnetDzList": (
                " & ".join(
                    [f"{props.magnet.dz}" for props in cas220103.magnet_properties]
                )
            ),
            "currentSupplyList": (
                " & ".join(
                    [f"{props.current_supply}" for props in cas220103.magnet_properties]
                )
            ),
            "conductorCurrentDensityList": (
                " & ".join([f"{props.j_tape}" for props in cas220103.magnet_properties])
            ),
            "cableWidthList": (
                " & ".join(
                    [f"{props.cable_w}" for props in cas220103.magnet_properties]
                )
            ),
            "cableHeightList": (
                " & ".join(
                    [f"{props.cable_h}" for props in cas220103.magnet_properties]
                )
            ),
            "totalVolumeList": (
                " & ".join(
                    [f"{props.vol_coil}" for props in cas220103.magnet_properties]
                )
            ),
            "crossSectionalAreaList": (
                " & ".join(
                    [f"{props.cs_area}" for props in cas220103.magnet_properties]
                )
            ),
            "turnInsulationFractionList": (
                " & ".join(
                    [f"{props.magnet.frac_in}" for props in cas220103.magnet_properties]
                )
            ),
            "cableTurnsList": (
                " & ".join(
                    [f"{props.turns_c}" for props in cas220103.magnet_properties]
                )
            ),
            "totalTurnsOfConductorList": (
                " & ".join(
                    [f"{props.turns_scs}" for props in cas220103.magnet_properties]
                )
            ),
            "lengthOfConductorList": (
                " & ".join(
                    [f"{props.tape_length}" for props in cas220103.magnet_properties]
                )
            ),
            "currentPerConductorList": (
                " & ".join(
                    [
                        f"{props.max_tape_current}"
                        for props in cas220103.magnet_properties
                    ]
                )
            ),
            "costOfRebcoTapeList": (
                " & ".join(
                    [str(coils.m_cost_ybco) for _ in cas220103.magnet_properties]
                )
            ),
            "costOfScList": (
                " & ".join(
                    [f"{props.cost_sc}" for props in cas220103.magnet_properties]
                )
            ),
            "costOfCopperList": (
                " & ".join(
                    [f"{props.cost_cu}" for props in cas220103.magnet_properties]
                )
            ),
            "costOfStainlessSteelList": (
                " & ".join(
                    [f"{props.cost_ss}" for props in cas220103.magnet_properties]
                )
            ),
            "costOfTurnInsulationList": (
                " & ".join([f"{props.cost_i}" for props in cas220103.magnet_properties])
            ),
            "totalMaterialCostList": (
                " & ".join(
                    [f"{props.tot_mat_cost}" for props in cas220103.magnet_properties]
                )
            ),
            "manufacturingFactorList": (
                " & ".join([str(coils.mfr_factor) for _ in cas220103.magnet_properties])
            ),
            "structuralCostList": (
                " & ".join(
                    [
                        f"{props.magnet_struct_cost}"
                        for props in cas220103.magnet_properties
                    ]
                )
            ),
            "numberCoilsList": (
                " & ".join(
                    [
                        f"{props.magnet.coil_count}"
                        for props in cas220103.magnet_properties
                    ]
                )
            ),
            "magnetCostList": (
                " & ".join(
                    [f"{props.magnet_cost}" for props in cas220103.magnet_properties]
                )
            ),
            "magnetTotalCostIndividualList": (
                " & ".join(
                    [
                        f"{props.magnet_total_cost_individual}"
                        for props in cas220103.magnet_properties
                    ]
                )
            ),
            "magnetTotalCostList": (
                " & ".join(
                    [
                        f"{props.magnet_total_cost}"
                        for props in cas220103.magnet_properties
                    ]
                )
            ),
        }

    def _init_ife_lasers(
        self, cas220103: CAS220103Lasers, power_input: PowerInput, lasers: Lasers
    ):
        """Initialize for IFE lasers case."""
        if power_input is None or lasers is None:
            raise ValueError(
                "power_input and lasers must be provided for IFE reactor type"
            )

        self.template_file = "CAS220103_IFE_DT.tex"

        # Get replacements from NIF costs
        scaled_costs = get_nif_scaled_costs(power_input.p_implosion, lasers)
        self.replacements = get_nif_replacements(scaled_costs)
        self.replacements["C220103"] = str(round(cas220103.C220103))
