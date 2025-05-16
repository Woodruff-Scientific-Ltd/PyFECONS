from dataclasses import dataclass

from pyfecons.costing.categories.cas400000 import CAS40
from pyfecons.inputs.lsa_levels import LsaLevels
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS40Section(ReportSection):
    def __init__(self, cas40: CAS40, lsa_levels: LsaLevels):
        super().__init__()
        self.template_file = "CAS400000.tex"
        self.replacements = {
            "lsaLevel": lsa_levels.lsa,  # TODO - not in template
            "C400000LSA": str(round(cas40.C400000LSA)),
            "C400000XXX": str(round(cas40.C400000)),  # TODO - not in template
        }
