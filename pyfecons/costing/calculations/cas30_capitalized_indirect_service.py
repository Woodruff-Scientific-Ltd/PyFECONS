from pyfecons.costing.accounting.power_table import PowerTable
from pyfecons.costing.categories.cas200000 import CAS20
from pyfecons.costing.categories.cas300000 import CAS30
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.lsa_levels import LsaLevels
from pyfecons.units import M_USD


def cas30_capitalized_indirect_service_costs(
    basic: Basic, lsa_levels: LsaLevels, power_table: PowerTable, cas20: CAS20
) -> CAS30:
    # Cost Category 30 Capitalized Indirect Service Costs (CISC)
    cas30 = CAS30()
    p_net = power_table.p_net

    # Cost Category 31 – Field Indirect Costs - previously Cost Category 93
    # 0.060 * C_90; %NMOD*(/1e6)/A_power * A_C_93 #Field Office Engineering and Services  Table 3.2-VII of Ref. [1]
    cas30.C310000LSA = M_USD(lsa_levels.fac_93[lsa_levels.lsa - 1] * cas20.C200000)
    cas30.C310000 = M_USD(
        (p_net / 150) ** -0.5 * p_net * 0.02 * basic.construction_time
    )

    # Cost Category 32  – Construction Supervision - previously Cost Category 91
    cas30.C320000LSA = M_USD(lsa_levels.fac_91[lsa_levels.lsa - 1] * cas20.C200000)
    # this takes the 316$/kW and divides by 6 to obtain a cost per year of 0.053$/MW and applies to PE,
    # which is the net electric.  There are arguments that this should be applied to the gross electric,
    # if we consider demonstration plants, but this code is not set up for FOAK currently.
    cas30.C320000 = M_USD(
        (p_net / 150) ** -0.5 * p_net * 0.05 * basic.construction_time
    )

    # Cost Category 33 – Commissioning and Start-up Costs

    # Cost Category 34 – Demonstration Test Run

    # Cost Category 35 – Design Services Offsite
    cas30.C350000 = M_USD(
        (p_net / 150) ** -0.5 * p_net * 0.03 * basic.construction_time
    )
    # 0.052 * C_90; %NMOD*(/1e6)/A_power * A_C_92; %Home Office Engineering and Services  Table 3.2-VII of Ref. [1]
    cas30.C350000LSA = M_USD(lsa_levels.fac_92[lsa_levels.lsa - 1] * cas20.C200000)

    cas30.C300000 = M_USD(cas30.C310000 + cas30.C320000 + cas30.C350000)

    cas30.template_file = "CAS300000.tex"
    cas30.replacements = {
        "constructionTime": round(basic.construction_time),
        "C300000": round(cas30.C300000),  # TODO - not in template
        "C310000LSA": round(cas30.C310000LSA),
        "C310000XXX": round(cas30.C310000),
        "C320000": round(cas30.C320000),
        "C350000LSA": round(cas30.C350000LSA),
        "C350000XXX": round(cas30.C350000),
    }
    return cas30
