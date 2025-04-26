from dataclasses import dataclass
from typing import Dict, Any

from pyfecons.report.section import ReportSection
from pyfecons.costing.categories.cas220102 import CAS220102
from pyfecons.enums import ReactorType


@dataclass
class CAS220102Section(ReportSection):
    def __init__(self, cas220102: CAS220102, reactor_type: ReactorType):
        super().__init__()
        self.template_file = "CAS220102.tex"

        # Base replacements that are common for all reactor types
        self.replacements = {
            "C22010201": str(round(cas220102.C22010201, 1)),
            "C22010202": str(round(cas220102.C22010202, 1)),
            "C22010203": str(round(cas220102.C22010203, 1)),
            "C22010204": str(round(cas220102.C22010204, 1)),
            "C220102XX": str(round(cas220102.C220102, 1)),
            "V220102": str(round(cas220102.V_HTS, 1)),
            "VOL9": str(round(cas220102.V_HTS, 1)),
        }

        # Add reactor-specific volume replacements
        if reactor_type == ReactorType.IFE:
            self.replacements.update(
                {
                    "VOL10": str(
                        round(cas220102.V_HTS, 1)
                    ),  # For IFE, use V_HTS for VOL10
                    "VOL14": str(
                        round(cas220102.V_HTS, 1)
                    ),  # For IFE, use V_HTS for VOL14
                }
            )
        elif reactor_type == ReactorType.MFE:
            self.replacements.update(
                {
                    "VOL11": str(
                        round(cas220102.V_HTS, 1)
                    ),  # For MFE, use V_HTS for VOL11
                }
            )
