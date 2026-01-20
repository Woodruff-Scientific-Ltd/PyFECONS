from pyfecons.costing.categories.cas100000 import CAS10
from pyfecons.inputs.basic import Basic
from pyfecons.report import ReportSection


class CAS10Section(ReportSection):
    def __init__(self, cas10: CAS10, basic: Basic):
        super().__init__()
        self.template_file = "CAS100000.tex"
        self.replacements = {
            "Nmod": str(basic.n_mod),
            "C100000": str(cas10.C100000),
            "C110100": str(cas10.C110100),
            "C110200": str(cas10.C110200),
            "C110000": str(cas10.C110000),
            "C120000": str(cas10.C120000),
            "C130000": str(cas10.C130000),
            "C140000": str(cas10.C140000),
            "C150000": str(cas10.C150000),
            "C160000": str(cas10.C160000),
            "C170000": str(cas10.C170000),
            "C190000": str(cas10.C190000),
        }
