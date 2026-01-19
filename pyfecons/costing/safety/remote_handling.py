from pyfecons.costing.categories.cas220606 import CAS220606
from pyfecons.enums import FusionMachineType
from pyfecons.inputs.basic import Basic
from pyfecons.units import M_USD

# Contract value for ITER divertor remote handling system
# Source:
# Contract for Iter Remote Handling System (no date) Contract for Iter remote handling system - World Nuclear News.
ITER_REMOTE_HANDLING_SYSTEM_COST_USD = 55_000_000.0


def cas_220606_remote_handling_costs(basic: Basic) -> CAS220606:
    """
    Calculates the cost for the Remote Handling System (Cost Category 22.06.06).

    The cost basis is derived from the ITER divertor remote handling system contract,
    valued at approximately 40 million EUR (~55 million USD). This is treated as a
    fixed cost allocated to magnetically confined fusion machines (MFE) and only
    included when safety and hazard mitigation costs are enabled.

    :param basic: Basic input parameters including fusion_machine_type and safety flag.
    :return: CAS220606 object with the calculated cost.
    """
    cas220606 = CAS220606()

    if (
        basic.include_safety_hazards_costs
        and basic.fusion_machine_type == FusionMachineType.MFE
    ):
        cas220606.C220606 = M_USD(ITER_REMOTE_HANDLING_SYSTEM_COST_USD / 1e6)
    else:
        cas220606.C220606 = M_USD(0.0)

    return cas220606
