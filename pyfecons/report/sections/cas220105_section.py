from dataclasses import dataclass

from pyfecons.costing.categories.cas220105 import CAS220105
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.primary_structure import PrimaryStructure
from pyfecons.report.section import ReportSection


@dataclass
class CAS220105Section(ReportSection):
    """Report section for CAS220105 primary structure."""

    def __init__(
        self, cas220105: CAS220105, basic: Basic, primary_structure: PrimaryStructure
    ):
        super().__init__()
        self.template_file = "CAS220105.tex"
        self.replacements = {
            "C22010501": str(round(cas220105.C22010501)),
            "C22010502": str(round(cas220105.C22010502)),
            "C22010500": str(round(cas220105.C220105)),
            "systPGA": str(round(primary_structure.syst_pga.value, 1)),
            "PNRL": str(round(basic.p_nrl)),
        }
