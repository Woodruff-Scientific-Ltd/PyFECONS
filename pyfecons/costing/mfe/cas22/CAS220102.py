from pyfecons.costing.calculations.conversions import k_to_m_usd
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.materials import Materials
from pyfecons.units import M_USD

materials = Materials()


def cas_220102_shield(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.2: Shield
    OUT = data.cas220102
    cas220101 = data.cas220101
    shield = inputs.shield

    # Retrieve the volume of HTS from the reactor_volumes dictionary
    OUT.V_HTS = round(cas220101.ht_shield_vol, 1)

    # Calculate the cost for HTS
    C_HTS = round(OUT.V_HTS * (
            materials.SiC.rho * materials.SiC.c_raw * materials.SiC.m * shield.f_SiC +
            materials.PbLi.rho * materials.PbLi.c * shield.FPCPPFbLi +
            materials.W.rho * materials.W.c_raw * materials.W.m * shield.f_W +
            materials.BFS.rho * materials.BFS.c_raw * materials.BFS.m * shield.f_BFS
    ) / 1e6, 1)

    # Volume of HTShield that is BFS
    # TODO this is unused
    V_HTS_BFS = OUT.V_HTS * shield.f_BFS

    # The cost C_22_1_2 is the same as C_HTS
    OUT.C22010201 = M_USD(round(C_HTS, 1))
    OUT.C22010202 = k_to_m_usd(cas220101.lt_shield_vol * materials.SS316.c_raw * materials.SS316.m)
    OUT.C22010203 = k_to_m_usd(cas220101.bioshield_vol * materials.SS316.c_raw * materials.SS316.m)
    OUT.C22010204 = M_USD(OUT.C22010203 * 0.1)
    OUT.C220102 = M_USD(OUT.C22010201 + OUT.C22010202 + OUT.C22010203 + OUT.C22010204)

    OUT.template_file = 'CAS220102.tex'
    OUT.replacements = {
        'C220102__': round(data.cas220102.C220102),
        'C22010201': round(data.cas220102.C22010201),
        'C22010202': round(data.cas220102.C22010202),
        'C22010203': round(data.cas220102.C22010203),
        'C22010204': round(data.cas220102.C22010204),
        'V220102': round(data.cas220102.V_HTS),  # Missing from CAS220102.tex
        'primaryC': inputs.blanket.primary_coolant.display_name,
        'VOL9': round(data.cas220101.ht_shield_vol),
        'VOL11': round(data.cas220101.lt_shield_vol),  # Missing from CAS220102.tex
    }
    return OUT
