from pyfecons.data import CAS22, Data
from pyfecons.materials import Materials
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


def compute_replacements(data: Data):
    return {
        'C220000': round(data.cas22.C220000, 2),  # TODO - not in the template
        'FSrho': round(Materials.FERRITIC_STEEL.rho, 2),
        'FScraw': round(Materials.FERRITIC_STEEL.c_raw, 2),
        'FSm': round(Materials.FERRITIC_STEEL.m, 2),
        'FSsigma': round(Materials.FERRITIC_STEEL.sigma, 2),
        'Pbrho': round(Materials.LEAD.rho, 2),
        'Pbcraw': round(Materials.LEAD.c_raw, 2),
        'Pbm': round(Materials.LEAD.m, 2),
        'Li4SiO4rho': round(Materials.LITHIUM_SILICATE.rho, 2),
        'Li4SiO4craw': round(Materials.LITHIUM_SILICATE.c_raw, 2),
        'Li4SiO4m': round(Materials.LITHIUM_SILICATE.m, 2),
        'Fliberho': round(Materials.FLIBE.rho, 2),
        'Flibec': round(Materials.FLIBE.c, 2),
        'Wrho': round(Materials.TUNGSTEN.rho, 2),
        'Wcraw': round(Materials.TUNGSTEN.c_raw, 2),
        'Wm': round(Materials.TUNGSTEN.m, 2),
        'Lirho': round(Materials.LITHIUM.rho, 2),
        'Licraw': round(Materials.LITHIUM.c_raw, 2),
        'Lim': round(Materials.LITHIUM.m, 2),
        'BFSrho': round(Materials.BFS.rho, 2),
        'BFScraw': round(Materials.BFS.c_raw, 2),
        'BFSm': round(Materials.BFS.m, 2),
        'PbLirho': round(Materials.PBLI.rho, 2),
        'PbLic': round(Materials.PBLI.c, 2),
        'SiCrho': round(Materials.SILICON_CARBIDE.rho, 2),
        'SiCcraw': round(Materials.SILICON_CARBIDE.c_raw, 2),
        'SiCm': round(Materials.SILICON_CARBIDE.m, 2),
        'Inconelrho': round(Materials.INCONEL.rho, 2),
        'Inconelcraw': round(Materials.INCONEL.c_raw, 2),
        'Inconelm': round(Materials.INCONEL.m, 2),
        'Curho': round(Materials.COPPER.rho, 2),
        'Cucraw': round(Materials.COPPER.c_raw, 2),
        'Cum': round(Materials.COPPER.m, 2),
        'Polyimiderho': round(Materials.POLYIMIDE.rho, 2),
        'Polyimidecraw': round(Materials.POLYIMIDE.c_raw, 2),
        'Polyimidem': round(Materials.POLYIMIDE.m, 2),
        'YBCOrho': round(Materials.YBCO.rho, 2),
        'YBCOc': round(Materials.YBCO.c, 2),
        'Concreterho': round(Materials.CONCRETE.rho, 2),
        'Concretecraw': round(Materials.CONCRETE.c_raw, 2),
        'Concretem': round(Materials.CONCRETE.m, 2),
        'SS316rho': round(Materials.STAINLESS_STEEL_SS316.rho, 2),
        'SS316craw': round(Materials.STAINLESS_STEEL_SS316.c_raw, 2),
        'SS316m': round(Materials.STAINLESS_STEEL_SS316.m, 2),
        'SS316sigma': round(Materials.STAINLESS_STEEL_SS316.sigma, 2),
        'Nb3Snc': round(Materials.NB3SN.c, 2),
        'Incoloyrho': round(Materials.INCOLOY.rho, 2),
        'Incoloycraw': round(Materials.INCOLOY.c_raw, 2),
        'Incoloym': round(Materials.INCOLOY.m, 2),
    }
