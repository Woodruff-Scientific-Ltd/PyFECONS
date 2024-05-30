from pyfecons.data import CAS22, Data
from pyfecons.inputs import Inputs
from pyfecons.units import M_USD


def compute_total_costs(OUT: CAS22, data: Data):
    # Cost category 22.1 total
    # TODO - I added C220119 since it's zero now, is this OK?
    OUT.C220100 = M_USD(data.cas220101.C220101 + data.cas220102.C220102 + data.cas220103.C220103
                        + data.cas220104.C220104 + data.cas220105.C220105 + data.cas220106.C220106
                        + data.cas220107.C220107 + data.cas220111.C220111 + data.cas220119.C220119)

    # Cost category 22.2 total
    OUT.C220000 = M_USD(OUT.C220100 + data.cas2202.C220200 + data.cas2203.C220300 + data.cas2204.C220400
                        + data.cas2205.C220500 + data.cas2206.C220600 + data.cas2207.C220700)
    return OUT


def compute_replacements(inputs: Inputs, data: Data):
    return {
        'C220000': round(data.cas22.C220000, 2),  # TODO - not in the template
        'FSrho': round(inputs.materials.FS.rho, 2),
        'FScraw': round(inputs.materials.FS.c_raw, 2),
        'FSm': round(inputs.materials.FS.m, 2),
        'FSsigma': round(inputs.materials.FS.sigma, 2),
        'Pbrho': round(inputs.materials.Pb.rho, 2),
        'Pbcraw': round(inputs.materials.Pb.c_raw, 2),
        'Pbm': round(inputs.materials.Pb.m, 2),
        'Li4SiO4rho': round(inputs.materials.Li4SiO4.rho, 2),
        'Li4SiO4craw': round(inputs.materials.Li4SiO4.c_raw, 2),
        'Li4SiO4m': round(inputs.materials.Li4SiO4.m, 2),
        'Fliberho': round(inputs.materials.FliBe.rho, 2),
        'Flibec': round(inputs.materials.FliBe.c, 2),
        'Wrho': round(inputs.materials.W.rho, 2),
        'Wcraw': round(inputs.materials.W.c_raw, 2),
        'Wm': round(inputs.materials.W.m, 2),
        'Lirho': round(inputs.materials.Li.rho, 2),
        'Licraw': round(inputs.materials.Li.c_raw, 2),
        'Lim': round(inputs.materials.Li.m, 2),
        'BFSrho': round(inputs.materials.BFS.rho, 2),
        'BFScraw': round(inputs.materials.BFS.c_raw, 2),
        'BFSm': round(inputs.materials.BFS.m, 2),
        'PbLirho': round(inputs.materials.PbLi.rho, 2),
        'PbLic': round(inputs.materials.PbLi.c, 2),
        'SiCrho': round(inputs.materials.SiC.rho, 2),
        'SiCcraw': round(inputs.materials.SiC.c_raw, 2),
        'SiCm': round(inputs.materials.SiC.m, 2),
        'Inconelrho': round(inputs.materials.Inconel.rho, 2),
        'Inconelcraw': round(inputs.materials.Inconel.c_raw, 2),
        'Inconelm': round(inputs.materials.Inconel.m, 2),
        'Curho': round(inputs.materials.Cu.rho, 2),
        'Cucraw': round(inputs.materials.Cu.c_raw, 2),
        'Cum': round(inputs.materials.Cu.m, 2),
        'Polyimiderho': round(inputs.materials.Polyimide.rho, 2),
        'Polyimidecraw': round(inputs.materials.Polyimide.c_raw, 2),
        'Polyimidem': round(inputs.materials.Polyimide.m, 2),
        'YBCOrho': round(inputs.materials.YBCO.rho, 2),
        'YBCOc': round(inputs.materials.YBCO.c, 2),
        'Concreterho': round(inputs.materials.Concrete.rho, 2),
        'Concretecraw': round(inputs.materials.Concrete.c_raw, 2),
        'Concretem': round(inputs.materials.Concrete.m, 2),
        'SS316rho': round(inputs.materials.SS316.rho, 2),
        'SS316craw': round(inputs.materials.SS316.c_raw, 2),
        'SS316m': round(inputs.materials.SS316.m, 2),
        'SS316sigma': round(inputs.materials.SS316.sigma, 2),
        'Nb3Snc': round(inputs.materials.Nb3Sn.c, 2),
        'Incoloyrho': round(inputs.materials.Incoloy.rho, 2),
        'Incoloycraw': round(inputs.materials.Incoloy.c_raw, 2),
        'Incoloym': round(inputs.materials.Incoloy.m, 2),
    }
