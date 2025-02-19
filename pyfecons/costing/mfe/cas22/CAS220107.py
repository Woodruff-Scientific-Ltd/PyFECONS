from pyfecons.costing.calculations.conversions import eur_to_usd
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.units import M_USD


def cas_220107_power_supplies(inputs: Inputs, data: Data) -> TemplateProvider:
    IN = inputs.power_supplies
    OUT = data.cas220107

    # Cost Category 22.1.7 Power supplies
    OUT.C22010701 = M_USD(data.power_table.p_coils * IN.cost_per_watt)

    # Scaled relative to ITER for a 500MW fusion power system
    # TODO where does 1552.24 and 269.6 come from?
    # kIUA exchange rate in USD
    kIUA = eur_to_usd(1552.24 * 1e-3)
    OUT.C22010702 = M_USD(269.6 * inputs.basic.p_nrl / 500 * IN.learning_credit * kIUA)
    OUT.C220107 = M_USD(OUT.C22010701 + OUT.C22010702)

    OUT.template_file = "CAS220107_MFE.tex"
    OUT.replacements = {
        "C22010700": round(OUT.C220107),
        "C22010701": round(OUT.C22010701),
        "C22010702": round(OUT.C22010702),
        "PNRL": round(inputs.basic.p_nrl),
    }
    return OUT
