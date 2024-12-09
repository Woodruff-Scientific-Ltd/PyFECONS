from pyfecons.data import Data, TemplateProvider, CAS220104SupplementaryHeating
from pyfecons.helpers import safe_round
from pyfecons.inputs import Inputs
from pyfecons.units import M_USD


def cas_220104_supplementary_heating(inputs: Inputs, data: Data) -> TemplateProvider:
    # 22.1.4 Supplementary heating
    IN = inputs.supplementary_heating
    OUT: CAS220104SupplementaryHeating = data.cas220104
    assert isinstance(OUT, CAS220104SupplementaryHeating)

    OUT.C22010401 = M_USD(IN.average_nbi.cost_2023 * IN.nbi_power)
    OUT.C22010402 = M_USD(IN.average_icrf.cost_2023 * IN.icrf_power)
    OUT.C220104 = M_USD(OUT.C22010401 + OUT.C22010402)

    heating_table_rows = "\n".join(
        [
            f"        {ref.name} & {ref.type} & {round(ref.power, 2)} "
            + f"& {safe_round(ref.cost_2009, 2)} & {round(ref.cost_2023, 2)} \\\\"
            for ref in IN.heating_refs()
        ]
    )

    OUT.template_file = "CAS220104_MFE_DT.tex"
    OUT.replacements = {
        "C22010401": str(round(OUT.C22010401, 3)),
        "C22010402": str(round(OUT.C22010402, 3)),
        "C220104__": str(round(OUT.C220104, 3)),
        "NBIPOWER": str(round(IN.nbi_power, 3)),
        "ICRFPOWER": str(round(IN.icrf_power, 3)),
        "HEATING_TABLE_ROWS": heating_table_rows,
    }
    return OUT
