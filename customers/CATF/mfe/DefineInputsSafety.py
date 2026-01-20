"""
Safety-specific DefineInputs for CATF MFE.

This module reuses the baseline CATF MFE DefineInputs.Generate() and only
applies safety-related tweaks (flags + extra inputs) to avoid duplicating
the core configuration.
"""

from pyfecons.enums import Region
from pyfecons.inputs.tritium_release import TritiumRelease
from customers.CATF.mfe.DefineInputs import Generate as _GenerateBase


def Generate():
    """
    Return an AllInputs instance identical to the baseline CATF MFE
    configuration, but with safety / hazard mitigation enabled and
    safety-specific parameters populated.
    """

    inputs = _GenerateBase()

    # Turn on safety & hazard mitigation costs for this run.
    inputs.basic.include_safety_hazards_costs = True

    # Safety runs are currently parameterized for a US site; this drives
    # region-dependent licensing and tritium land add-ons.
    inputs.basic.region = Region.US

    inputs.tritium_release = TritiumRelease(
        # Total HTO inventory [g] based on DEMO-like scenario in
        # Lukacs & Williams (2020), as used in catf_ongoing_changes.py.
        hto_inventory_g=4700.0,
        # Dust tritium inventory [g/month]; 689 kg/year / 12 months, see
        # Lukacs & Williams (2020) and catf_ongoing_changes.py.
        dust_tritium_inventory_g_per_month=689000.0 / 12.0,
        # Representative stack height [m] used for polynomial fits
        # in the same study (20 m release case).
        stack_height_m=20.0,
    )

    return inputs

