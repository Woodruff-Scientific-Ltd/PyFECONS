from pyfecons.costing.categories.cas220104_supplementary_heating import (
    CAS220104SupplementaryHeating,
)
from pyfecons.inputs.supplementary_heating import SupplementaryHeating
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
    return cas220104
