from dataclasses import dataclass
from typing import Dict, Any

from pyfecons.report.section import ReportSection
from pyfecons.costing.categories.cas220101 import CAS220101
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.blanket import Blanket
from pyfecons.inputs.radial_build import RadialBuild
from pyfecons.enums import ReactorType
from pyfecons.figures import RadialBuildPlotter


def get_template_file(reactor_type: ReactorType):
    if reactor_type == ReactorType.MFE:
        return "CAS220101_MFE_DT.tex"
    if reactor_type == ReactorType.IFE:
        return "CAS220101_IFE_DT.tex"
    raise ValueError(f"Unsupported reactor type {reactor_type}")


def compute_220101_replacements(
    reactor_type: ReactorType, blanket: Blanket, IN: RadialBuild, OUT: CAS220101
) -> Dict[str, str]:
    rounding = 2
    return {
        "C22010100": str(OUT.C220101),
        "C22010101": str(OUT.C22010101),
        "C22010102": str(OUT.C22010102),
        "primaryC": blanket.primary_coolant.display_name,
        "secondaryC": blanket.secondary_coolant.display_name,
        "neutronM": blanket.neutron_multiplier.display_name,
        "structure1": blanket.structure.display_name,
        "firstW": blanket.first_wall.display_name,
        "TH01": round(IN.plasma_t, rounding),
        "TH02": round(IN.vacuum_t, rounding),
        "TH03": round(IN.firstwall_t, rounding),
        "TH04": round(IN.blanket1_t, rounding),
        "TH05": round(IN.structure_t, rounding),
        "TH06": round(IN.reflector_t, rounding),
        "TH07": round(IN.gap1_t, rounding),
        "TH08": round(IN.vessel_t, rounding),
        "TH09": round(IN.ht_shield_t, rounding),
        "TH10": round(IN.lt_shield_t, rounding),
        **(
            {"TH11": round(IN.coil_t, rounding)}
            if reactor_type == ReactorType.MFE
            else {}
        ),
        "TH12": round(IN.axis_t, rounding),
        "TH13": round(IN.gap2_t, rounding),
        "TH14": round(IN.bioshield_t, rounding),
        "RAD1I": round(OUT.plasma_ir, rounding),
        "RAD2I": round(OUT.vacuum_ir, rounding),
        "RAD3I": round(OUT.firstwall_ir, rounding),
        "RAD4I": round(OUT.blanket1_ir, rounding),
        "RAD5I": round(OUT.structure_ir, rounding),
        "RAD6I": round(OUT.reflector_ir, rounding),
        "RAD7I": round(OUT.gap1_ir, rounding),
        "RAD8I": round(OUT.vessel_ir, rounding),
        "RAD9I": round(OUT.ht_shield_ir, rounding),
        "RAD10I": round(OUT.lt_shield_ir, rounding),
        **(
            {"RAD11I": round(OUT.coil_ir, rounding)}
            if reactor_type == ReactorType.MFE
            else {}
        ),
        "RAD12I": round(OUT.axis_ir, rounding),
        "RAD13I": round(OUT.gap2_ir, rounding),
        "RAD14I": round(OUT.bioshield_ir, rounding),
        "RAD1O": round(OUT.plasma_or, rounding),
        "RAD2O": round(OUT.vacuum_or, rounding),
        "RAD3O": round(OUT.firstwall_or, rounding),
        "RAD4O": round(OUT.blanket1_or, rounding),
        "RAD5O": round(OUT.structure_or, rounding),
        "RAD6O": round(OUT.reflector_or, rounding),
        "RAD7O": round(OUT.gap1_or, rounding),
        "RAD8O": round(OUT.vessel_or, rounding),
        "RAD9O": round(OUT.ht_shield_or, rounding),
        "RAD10O": round(OUT.lt_shield_or, rounding),
        **(
            {"RAD11O": round(OUT.coil_or, rounding)}
            if reactor_type == ReactorType.MFE
            else {}
        ),
        "RAD12O": round(OUT.axis_or, rounding),
        "RAD13O": round(OUT.gap2_or, rounding),
        "RAD14O": round(OUT.bioshield_or, rounding),
        "VOL01": round(OUT.plasma_vol, rounding),
        "VOL02": round(OUT.vacuum_vol, rounding),
        "VOL03": round(OUT.firstwall_vol, rounding),
        "VOL04": round(OUT.blanket1_vol, rounding),
        "VOL05": round(OUT.structure_vol, rounding),
        "VOL06": round(OUT.reflector_vol, rounding),
        "VOL07": round(OUT.gap1_vol, rounding),
        "VOL08": round(OUT.vessel_vol, rounding),
        "VOL09": round(OUT.ht_shield_vol, rounding),
        "VOL10": round(OUT.lt_shield_vol, rounding),
        **(
            {"VOL11": round(OUT.coil_vol, rounding)}
            if reactor_type == ReactorType.MFE
            else {}
        ),
        "VOL12": round(OUT.axis_vol, rounding),
        "VOL13": round(OUT.gap2_vol, rounding),
        "VOL14": round(OUT.bioshield_vol, rounding),
    }


@dataclass
class CAS220101Section(ReportSection):
    """Report section for CAS220101 (First Wall and Blanket) data."""

    def __init__(
        self, cas220101: CAS220101, basic: Basic, radial_build: RadialBuild, blanket: Blanket
    ):
        super().__init__()
        self.template_file = get_template_file(basic.reactor_type)
        self.figures["Figures/radial_build.pdf"] = RadialBuildPlotter.plot(basic.reactor_type, radial_build)
        self.replacements = compute_220101_replacements(basic.reactor_type, blanket, radial_build, cas220101) 