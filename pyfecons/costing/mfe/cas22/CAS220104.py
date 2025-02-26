from pyfecons.costing.categories.cas220104_supplementary_heating import CAS220104SupplementaryHeating
from pyfecons.inputs.supplementary_heating import SupplementaryHeating
from pyfecons.helpers import safe_round
from pyfecons.units import M_USD


def cas_220104_supplementary_heating_costs(
    supplementary_heating: SupplementaryHeating,
) -> CAS220104SupplementaryHeating:
    # 22.1.4 Supplementary heating
    heating = supplementary_heating
    cas220104 = CAS220104SupplementaryHeating()
    assert isinstance(cas220104, CAS220104SupplementaryHeating)

    cas220104.C22010401 = M_USD(heating.average_nbi.cost_2023 * heating.nbi_power)
    cas220104.C22010402 = M_USD(heating.average_icrf.cost_2023 * heating.icrf_power)
    cas220104.C220104 = M_USD(cas220104.C22010401 + cas220104.C22010402)

    heating_table_rows = "\n".join(
        [
            f"        {ref.name} & {ref.type} & {round(ref.power, 2)} "
            + f"& {safe_round(ref.cost_2009, 2)} & {round(ref.cost_2023, 2)} \\\\"
            for ref in heating.heating_refs()
        ]
    )

    cas220104.template_file = "CAS220104_MFE_DT.tex"
    cas220104.replacements = {
        "C22010401": str(round(cas220104.C22010401, 3)),
        "C22010402": str(round(cas220104.C22010402, 3)),
        "C220104__": str(round(cas220104.C220104, 3)),
        "NBIPOWER": str(round(heating.nbi_power, 3)),
        "ICRFPOWER": str(round(heating.icrf_power, 3)),
        "HEATING_TABLE_ROWS": heating_table_rows,
    }
    return cas220104
