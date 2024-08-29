from pyfecons.costing.calculations.conversions import k_to_m_usd
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.materials import Materials
from pyfecons.units import M_USD


def cas_220102_shield(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.2: Shield
    OUT = data.cas220102
    cas220101 = data.cas220101
    shield = inputs.shield

    # Retrieve the volume of HTS from the reactor_volumes dictionary
    OUT.V_HTS = round(cas220101.ht_shield_vol, 1)

    # Calculate the cost for HTS
    C_HTS = round(OUT.V_HTS * (
            Materials.SILICON_CARBIDE.rho * Materials.SILICON_CARBIDE.c_raw * Materials.SILICON_CARBIDE.m * shield.f_SiC +
            Materials.PBLI.rho * Materials.PBLI.c * shield.FPCPPFbLi +
            Materials.TUNGSTEN.rho * Materials.TUNGSTEN.c_raw * Materials.TUNGSTEN.m * shield.f_W +
            Materials.BFS.rho * Materials.BFS.c_raw * Materials.BFS.m * shield.f_BFS
    ) / 1e6, 1)

    # Volume of HTShield that is BFS
    # TODO this is unused
    V_HTS_BFS = OUT.V_HTS * shield.f_BFS

    # The cost C_22_1_2 is the same as C_HTS
    # TODO what's the *5 for?
    OUT.C22010201 = M_USD(round(C_HTS * 5, 1))
    OUT.C22010202 = k_to_m_usd(cas220101.lt_shield_vol * Materials.STAINLESS_STEEL_SS316.c_raw * Materials.STAINLESS_STEEL_SS316.m)
    OUT.C22010203 = k_to_m_usd(cas220101.bioshield_vol * Materials.STAINLESS_STEEL_SS316.c_raw * Materials.STAINLESS_STEEL_SS316.m)
    OUT.C22010204 = M_USD(OUT.C22010203 * 0.1)
    OUT.C220102 = M_USD(OUT.C22010201 + OUT.C22010202 + OUT.C22010203 + OUT.C22010204)

    OUT.template_file = 'CAS220102.tex'
    OUT.replacements = {
        'C22010201': round(OUT.C22010201),
        'C22010202': round(OUT.C22010202),
        'C22010203': round(OUT.C22010203),
        'C22010204': round(OUT.C22010204),
        'C220102XX': round(OUT.C220102),
        'V220102': round(OUT.V_HTS),  # TODO not in template
        'primaryC': inputs.blanket.primary_coolant.display_name,
        'VOL9': round(data.cas220101.ht_shield_vol),
        'VOL10': round(data.cas220101.lt_shield_vol),
        'VOL14': round(data.cas220101.bioshield_vol),  # TODO not in template
    }
    return OUT
