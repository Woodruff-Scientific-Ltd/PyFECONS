from pyfecons.costing.calculations.cas22.cas220105_primary_structure import (
    compute_engineering_costs,
    compute_fabrication_costs,
)
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.units import M_USD


def cas_220105_primary_structure(inputs: AllInputs, data: Data) -> TemplateProvider:
    # 22.1.5 primary structure
    OUT = data.cas220105

    OUT.C22010501 = compute_engineering_costs(
        inputs.primary_structure, data.power_table
    )
    OUT.C22010502 = compute_fabrication_costs(
        inputs.primary_structure, data.power_table
    )

    # total cost calculation
    OUT.C220105 = M_USD(OUT.C22010501 + OUT.C22010502)
    OUT.template_file = "CAS220105.tex"
    OUT.replacements = {
        "C22010501": str(round(OUT.C22010501)),
        "C22010502": str(round(OUT.C22010502)),
        "C22010500": str(round(OUT.C220105)),
        "systPGA": str(round(inputs.primary_structure.syst_pga.value, 1)),
        "PNRL": str(round(inputs.basic.p_nrl)),
    }
    return OUT
