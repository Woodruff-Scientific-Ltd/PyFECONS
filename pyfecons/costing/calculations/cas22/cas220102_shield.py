from pyfecons.costing.calculations.conversions import k_to_m_usd
from pyfecons.costing.categories.cas220101 import CAS220101
from pyfecons.costing.categories.cas220102 import CAS220102
from pyfecons.enums import ReactorType
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.blanket import Blanket
from pyfecons.inputs.shield import Shield
from pyfecons.materials import Materials
from pyfecons.units import M_USD

materials = Materials()


def cas_220102_shield_costs(
    basic: Basic, shield: Shield, blanket: Blanket, cas220101: CAS220101
) -> CAS220102:
    # Cost Category 22.1.2: Shield
    reactor_type = basic.reactor_type
    cas220102 = CAS220102()

    # Retrieve the volume of HTS from the reactor_volumes dictionary
    cas220102.V_HTS = round(cas220101.ht_shield_vol, 1)

    # Calculate the cost for HTS
    C_HTS = round(
        cas220102.V_HTS
        * (
            materials.SiC.rho * materials.SiC.c_raw * materials.SiC.m * shield.f_SiC
            + materials.PbLi.rho * materials.PbLi.c * shield.FPCPPFbLi
            + materials.W.rho * materials.W.c_raw * materials.W.m * shield.f_W
            + materials.BFS.rho * materials.BFS.c_raw * materials.BFS.m * shield.f_BFS
        )
        / 1e6,
        1,
    )

    # Volume of HTShield that is BFS
    # TODO this is unused
    V_HTS_BFS = cas220102.V_HTS * shield.f_BFS

    # The cost C_22_1_2 is the same as C_HTS
    # TODO what's the *5 for?
    c_hts_scaling = 5.0 if reactor_type == ReactorType.IFE else 1.0
    cas220102.C22010201 = M_USD(round(C_HTS * c_hts_scaling, 1))
    cas220102.C22010202 = k_to_m_usd(
        cas220101.lt_shield_vol * materials.SS316.c_raw * materials.SS316.m
    )
    cas220102.C22010203 = k_to_m_usd(
        cas220101.bioshield_vol * materials.SS316.c_raw * materials.SS316.m
    )
    cas220102.C22010204 = M_USD(cas220102.C22010203 * 0.1)
    cas220102.C220102 = M_USD(
        cas220102.C22010201
        + cas220102.C22010202
        + cas220102.C22010203
        + cas220102.C22010204
    )

    cas220102.template_file = "CAS220102.tex"
    cas220102.replacements = {
        "C22010201": round(cas220102.C22010201),
        "C22010202": round(cas220102.C22010202),
        "C22010203": round(cas220102.C22010203),
        "C22010204": round(cas220102.C22010204),
        "C220102XX": round(cas220102.C220102),
        "V220102": round(cas220102.V_HTS),  # TODO not in template
        "primaryC": blanket.primary_coolant.display_name,
        "VOL9": round(cas220101.ht_shield_vol),
    }
    if reactor_type == ReactorType.IFE:
        cas220102.replacements["VOL10"] = round(cas220101.lt_shield_vol)
        cas220102.replacements["VOL14"] = round(
            cas220101.bioshield_vol
        )  # TODO not in template
    if reactor_type == ReactorType.MFE:
        cas220102.replacements["VOL11"] = round(
            cas220101.lt_shield_vol
        )  # TODO not in template
    return cas220102
