from pyfecons.data import CAS22, Data, TemplateProvider
from pyfecons.materials import Materials
from pyfecons.units import M_USD

materials = Materials()


def cas_2200_reactor_plant_equipment_total(data: Data) -> TemplateProvider:
    # Reactor Plant Equipment (RPE) total
    OUT = data.cas22
    OUT = compute_cas22_total_costs(OUT, data)
    OUT.template_file = "CAS220000.tex"
    OUT.replacements = compute_replacements(data)
    return OUT


def compute_cas2201_total_costs(data: Data) -> M_USD:
    return M_USD(
        data.cas220101.C220101
        + data.cas220102.C220102
        + data.cas220103.C220103
        + data.cas220104.C220104
        + data.cas220105.C220105
        + data.cas220106.C220106
        + data.cas220107.C220107
        + data.cas220108.C220108
        + data.cas220109.C220109
        + data.cas220111.C220111
        + data.cas220119.C220119
    )


def compute_cas22_total_costs(OUT: CAS22, data: Data) -> CAS22:
    # Cost category 22.1 total
    OUT.C220100 = compute_cas2201_total_costs(data)

    # Cost category 22.2 total
    OUT.C220000 = M_USD(
        OUT.C220100
        + data.cas2202.C220200
        + data.cas2203.C220300
        + data.cas2204.C220400
        + data.cas2205.C220500
        + data.cas2206.C220600
        + data.cas2207.C220700
    )
    return OUT


def compute_replacements(data: Data):
    return {
        "C220000": round(data.cas22.C220000, 2),  # TODO - not in the template
        "FSrho": round(materials.FS.rho, 2),
        "FScraw": round(materials.FS.c_raw, 2),
        "FSm": round(materials.FS.m, 2),
        "FSsigma": round(materials.FS.sigma, 2),
        "Pbrho": round(materials.Pb.rho, 2),
        "Pbcraw": round(materials.Pb.c_raw, 2),
        "Pbm": round(materials.Pb.m, 2),
        "Li4SiO4rho": round(materials.Li4SiO4.rho, 2),
        "Li4SiO4craw": round(materials.Li4SiO4.c_raw, 2),
        "Li4SiO4m": round(materials.Li4SiO4.m, 2),
        "Fliberho": round(materials.FliBe.rho, 2),
        "Flibec": round(materials.FliBe.c, 2),
        "Wrho": round(materials.W.rho, 2),
        "Wcraw": round(materials.W.c_raw, 2),
        "Wm": round(materials.W.m, 2),
        "Lirho": round(materials.Li.rho, 2),
        "Licraw": round(materials.Li.c_raw, 2),
        "Lim": round(materials.Li.m, 2),
        "BFSrho": round(materials.BFS.rho, 2),
        "BFScraw": round(materials.BFS.c_raw, 2),
        "BFSm": round(materials.BFS.m, 2),
        "PbLirho": round(materials.PbLi.rho, 2),
        "PbLic": round(materials.PbLi.c, 2),
        "SiCrho": round(materials.SiC.rho, 2),
        "SiCcraw": round(materials.SiC.c_raw, 2),
        "SiCm": round(materials.SiC.m, 2),
        "Inconelrho": round(materials.Inconel.rho, 2),
        "Inconelcraw": round(materials.Inconel.c_raw, 2),
        "Inconelm": round(materials.Inconel.m, 2),
        "Curho": round(materials.Cu.rho, 2),
        "Cucraw": round(materials.Cu.c_raw, 2),
        "Cum": round(materials.Cu.m, 2),
        "Polyimiderho": round(materials.Polyimide.rho, 2),
        "Polyimidecraw": round(materials.Polyimide.c_raw, 2),
        "Polyimidem": round(materials.Polyimide.m, 2),
        "YBCOrho": round(materials.YBCO.rho, 2),
        "YBCOc": round(materials.YBCO.c, 2),
        "Concreterho": round(materials.Concrete.rho, 2),
        "Concretecraw": round(materials.Concrete.c_raw, 2),
        "Concretem": round(materials.Concrete.m, 2),
        "SS316rho": round(materials.SS316.rho, 2),
        "SS316craw": round(materials.SS316.c_raw, 2),
        "SS316m": round(materials.SS316.m, 2),
        "SS316sigma": round(materials.SS316.sigma, 2),
        "Nb3Snc": round(materials.Nb3Sn.c, 2),
        "Incoloyrho": round(materials.Incoloy.rho, 2),
        "Incoloycraw": round(materials.Incoloy.c_raw, 2),
        "Incoloym": round(materials.Incoloy.m, 2),
    }
