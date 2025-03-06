from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.units import M_USD


def cas30_capitalized_indirect_service_costs(
    inputs: AllInputs, data: Data
) -> TemplateProvider:
    # Cost Category 30 Capitalized Indirect Service Costs (CISC)
    IN = inputs.lsa_levels
    OUT = data.cas30
    basic = inputs.basic
    p_net = data.power_table.p_net

    # Cost Category 31 – Field Indirect Costs - previously Cost Category 93
    # 0.060 * C_90; %NMOD*(/1e6)/A_power * A_C_93 #Field Office Engineering and Services  Table 3.2-VII of Ref. [1]
    OUT.C310000LSA = M_USD(IN.fac_93[IN.lsa - 1] * data.cas20.C200000)
    OUT.C310000 = M_USD((p_net / 150) ** -0.5 * p_net * 0.02 * basic.construction_time)

    # Cost Category 32  – Construction Supervision - previously Cost Category 91
    OUT.C320000LSA = M_USD(IN.fac_91[IN.lsa - 1] * data.cas20.C200000)
    # this takes the 316$/kW and divides by 6 to obtain a cost per year of 0.053$/MW and applies to PE,
    # which is the net electric.  There are arguments that this should be applied to the gross electric,
    # if we consider demonstration plants, but this code is not set up for FOAK currently.
    OUT.C320000 = M_USD((p_net / 150) ** -0.5 * p_net * 0.05 * basic.construction_time)

    # Cost Category 33 – Commissioning and Start-up Costs

    # Cost Category 34 – Demonstration Test Run

    # Cost Category 35 – Design Services Offsite
    OUT.C350000 = M_USD((p_net / 150) ** -0.5 * p_net * 0.03 * basic.construction_time)
    # 0.052 * C_90; %NMOD*(/1e6)/A_power * A_C_92; %Home Office Engineering and Services  Table 3.2-VII of Ref. [1]
    OUT.C350000LSA = M_USD(IN.fac_92[IN.lsa - 1] * data.cas20.C200000)

    OUT.C300000 = M_USD(OUT.C310000 + OUT.C320000 + OUT.C350000)

    OUT.template_file = "CAS300000.tex"
    OUT.replacements = {
        "constructionTime": round(basic.construction_time),
        "C300000": round(OUT.C300000),  # TODO - not in template
        "C310000LSA": round(OUT.C310000LSA),
        "C310000XXX": round(OUT.C310000),
        "C320000": round(OUT.C320000),
        "C350000LSA": round(OUT.C350000LSA),
        "C350000XXX": round(OUT.C350000),
    }
    return OUT
