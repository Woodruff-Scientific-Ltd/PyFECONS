from pyfecons.units import M_USD
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def cas_60(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 60 Capitalized Financial Costs (CFC)
    OUT = data.cas60
    financial = inputs.financial
    lsa = inputs.lsa_levels

    # Cost Category 61 – Escalation - formerly Cost Category 98: Escalation During Construction
    # Escalation during Construction (EDC) Table 3.2-X of Ref. [1]
    OUT.C610000 = M_USD(
        float(inputs.basic.n_mod)
        * inputs.basic.p_nrl
        / financial.a_power
        * financial.a_c_98
    )

    # Cost Category 63 – Interest During Construction (IDC) formerly cost category 97
    # for inflation rate = 0.05/y (cf. ARIES) and 0.02/y (lower and more modern).  The 0.05/y values check with Table 2.2-XVII p. 2-59 of the ARIES-II/IV report.
    # Construction lead time is varied between 3 and 12 years. STARFIRE (with a published schedule) and ARIES used 6 years, which could be considered optimistic for a (big) tokamak.  We might be able to defend a lower base time for the smaller ARPA-E cases invoking factory fabrication and modularity (already assumed by STARFIRE).
    # Your calculations so far have used the 6-yr f_IDC for 0.05/y inflation rate for Acct. 97; a sensitivity of TCC as a function of construction lead time is what we had in mind.
    # f_EDC for constant-dollar costing is zero.  Nominal- (then-current dollar) costing includes f_EDC in Acct. 98.
    # I am a bit surprised that the f_IDC for 0.02/y is slightly larger than the corresponding 0.05/y value.
    # f_IDC - Interest During Construction for constant dollars
    # f_EDC - Escalation During Construction
    # a sensitivity of TCC as a function of construction lead time is what we had in mind
    OUT.C630000LSA = M_USD(lsa.fac_97[lsa.lsa - 1] * data.cas20.C200000)

    # C_97_sens = costfac90 * (C_90 + C_96 + C_94 + C_93 + C_92 + C_91);
    # (/1e6)/A_power * A_C_97; %Interest during Construction (IDC)  Table 3.2-X of Ref. [1]
    OUT.C630000 = M_USD(data.power_table.p_net * 0.099 * inputs.basic.construction_time)

    OUT.C600000 = M_USD(OUT.C630000 + OUT.C610000)

    OUT.template_file = "CAS600000.tex"
    OUT.replacements = {
        "C600000": round(OUT.C600000),
        "C610000": round(OUT.C610000),
        "C630000LSA": round(OUT.C630000LSA),
        "C630000XXX": round(OUT.C630000),
    }
    return OUT
