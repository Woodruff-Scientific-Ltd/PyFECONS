from dataclasses import dataclass

from pyfecons.costing.categories.cas220500 import CAS2205
from pyfecons.inputs.fuel_handling import FuelHandling
from pyfecons.report.section import ReportSection


@dataclass
class CAS2205Section(ReportSection):
    def __init__(self, cas2205: CAS2205, fuel_handling: FuelHandling):
        super().__init__()
        self.template_file = "CAS220500_DT.tex"
        self.replacements = {
            "lcredit": str(round(fuel_handling.learning_curve_credit, 1)),
            "ltoak": str(round(fuel_handling.learning_tenth_of_a_kind, 1)),
            "C2205010ITER": str(round(cas2205.C2205010ITER, 1)),
            "C2205020ITER": str(round(cas2205.C2205020ITER, 1)),
            "C2205030ITER": str(round(cas2205.C2205030ITER, 1)),
            "C2205040ITER": str(round(cas2205.C2205040ITER, 1)),
            "C2205050ITER": str(round(cas2205.C2205050ITER, 1)),
            "C2205060ITER": str(round(cas2205.C2205060ITER, 1)),
            "C22050ITER": str(round(cas2205.C22050ITER, 1)),
            "C220501": str(round(cas2205.C220501, 1)),
            "C220502": str(round(cas2205.C220502, 1)),
            "C220503": str(round(cas2205.C220503, 1)),
            "C220504": str(round(cas2205.C220504, 1)),
            "C220505": str(round(cas2205.C220505, 1)),
            "C220506": str(round(cas2205.C220506, 1)),
            "C220500": str(round(cas2205.C220500, 1)),
        }
