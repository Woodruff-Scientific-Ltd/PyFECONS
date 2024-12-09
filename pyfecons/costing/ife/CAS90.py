from pyfecons.units import M_USD
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs


def cas_90(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 90: Annualized Financial Costs (AFC)
    OUT = data.cas90
    financial = inputs.financial

    # Total Capital costs 99
    OUT.C990000 = M_USD(
        data.cas10.C100000
        + data.cas20.C200000
        + data.cas30.C300000
        + data.cas40.C400000
        + data.cas50.C500000
        + data.cas60.C600000
    )

    OUT.C900000 = M_USD(financial.capital_recovery_factor * OUT.C990000)

    OUT.template_file = "CAS900000.tex"
    OUT.replacements = {"C900000": round(OUT.C900000)}
    return OUT
