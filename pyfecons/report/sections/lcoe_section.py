from dataclasses import dataclass

from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.categories.cas700000 import CAS70
from pyfecons.costing.categories.cas800000 import CAS80
from pyfecons.costing.categories.cas900000 import CAS90
from pyfecons.costing.categories.lcoe import LCOE
from pyfecons.inputs.basic import Basic
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class LcoeSection(ReportSection):
    def __init__(
        self,
        lcoe: LCOE,
        basic: Basic,
        power_table: PowerTable,
        cas70: CAS70,
        cas80: CAS80,
        cas90: CAS90,
    ):
        super().__init__()
        self.template_file = "LCOE.tex"
        self.replacements = {
            "C1000000": str(round(lcoe.C1000000, 1)),
            "C2000000": str(round(lcoe.C2000000, 1)),
            "C700000": str(round(cas70.C700000, 1)),
            "C800000": str(round(cas80.C800000, 1)),
            "C900000": str(round(cas90.C900000, 1)),
            "PNET": str(round(power_table.p_net, 3)),
            "lifeY": str(round(basic.plant_lifetime)),
            "yinflation": str(100 * round(basic.yearly_inflation, 3)),
            "PAVAIL": str(round(basic.plant_availability, 2)),
        }
