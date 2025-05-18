from dataclasses import dataclass

from pyfecons.costing.categories.cas220000 import CAS22
from pyfecons.materials import Materials
from pyfecons.report.section import ReportSection

materials = Materials()


@dataclass
class CAS22Section(ReportSection):
    def __init__(self, cas22: CAS22):
        super().__init__()
        self.template_file = "CAS220000.tex"
        self.replacements = {
            "C220000": str(round(cas22.C220000, 2)),  # TODO - not in the template
            "FSrho": str(round(materials.FS.rho, 2)),
            "FScraw": str(round(materials.FS.c_raw, 2)),
            "FSm": str(round(materials.FS.m, 2)),
            "FSsigma": str(round(materials.FS.sigma, 2)),
            "Pbrho": str(round(materials.Pb.rho, 2)),
            "Pbcraw": str(round(materials.Pb.c_raw, 2)),
            "Pbm": str(round(materials.Pb.m, 2)),
            "Li4SiO4rho": str(round(materials.Li4SiO4.rho, 2)),
            "Li4SiO4craw": str(round(materials.Li4SiO4.c_raw, 2)),
            "Li4SiO4m": str(round(materials.Li4SiO4.m, 2)),
            "Fliberho": str(round(materials.FliBe.rho, 2)),
            "Flibec": str(round(materials.FliBe.c, 2)),
            "Wrho": str(round(materials.W.rho, 2)),
            "Wcraw": str(round(materials.W.c_raw, 2)),
            "Wm": str(round(materials.W.m, 2)),
            "Lirho": str(round(materials.Li.rho, 2)),
            "Licraw": str(round(materials.Li.c_raw, 2)),
            "Lim": str(round(materials.Li.m, 2)),
            "BFSrho": str(round(materials.BFS.rho, 2)),
            "BFScraw": str(round(materials.BFS.c_raw, 2)),
            "BFSm": str(round(materials.BFS.m, 2)),
            "PbLirho": str(round(materials.PbLi.rho, 2)),
            "PbLic": str(round(materials.PbLi.c, 2)),
            "SiCrho": str(round(materials.SiC.rho, 2)),
            "SiCcraw": str(round(materials.SiC.c_raw, 2)),
            "SiCm": str(round(materials.SiC.m, 2)),
            "Inconelrho": str(round(materials.Inconel.rho, 2)),
            "Inconelcraw": str(round(materials.Inconel.c_raw, 2)),
            "Inconelm": str(round(materials.Inconel.m, 2)),
            "Curho": str(round(materials.Cu.rho, 2)),
            "Cucraw": str(round(materials.Cu.c_raw, 2)),
            "Cum": str(round(materials.Cu.m, 2)),
            "Polyimiderho": str(round(materials.Polyimide.rho, 2)),
            "Polyimidecraw": str(round(materials.Polyimide.c_raw, 2)),
            "Polyimidem": str(round(materials.Polyimide.m, 2)),
            "YBCOrho": str(round(materials.YBCO.rho, 2)),
            "YBCOc": str(round(materials.YBCO.c, 2)),
            "Concreterho": str(round(materials.Concrete.rho, 2)),
            "Concretecraw": str(round(materials.Concrete.c_raw, 2)),
            "Concretem": str(round(materials.Concrete.m, 2)),
            "SS316rho": str(round(materials.SS316.rho, 2)),
            "SS316craw": str(round(materials.SS316.c_raw, 2)),
            "SS316m": str(round(materials.SS316.m, 2)),
            "SS316sigma": str(round(materials.SS316.sigma, 2)),
            "Nb3Snc": str(round(materials.Nb3Sn.c, 2)),
            "Incoloyrho": str(round(materials.Incoloy.rho, 2)),
            "Incoloycraw": str(round(materials.Incoloy.c_raw, 2)),
            "Incoloym": str(round(materials.Incoloy.m, 2)),
        }
