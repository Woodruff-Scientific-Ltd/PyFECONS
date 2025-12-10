import numpy as np

from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.costing.categories.cas220101 import CAS220101
from pyfecons.costing.categories.cas220106 import CAS220106
from pyfecons.inputs.vacuum_system import VacuumSystem
from pyfecons.materials import Materials
from pyfecons.units import M_USD, USD, Kilograms, Meters3

materials = Materials()


# IFE vacuum system calculations
def cas_220106_vacuum_system_costs(
    vacuum_system: VacuumSystem, cas220101: CAS220101
) -> CAS220106:
    # 22.1.6 Vacuum system
    # 22.1.6.1 Vacuum Vessel
    cas220106 = CAS220106()
    build = cas220101

    # Calculate mass and cost
    cas220106.material_volume = build.vessel_vol
    cas220106.mass_struct = Kilograms(cas220106.material_volume * materials.SS316.rho)
    # vessel material cost
    cas220106.ves_mat_cost = USD(materials.SS316.c_raw * cas220106.mass_struct)
    # internal volume of the vacuum vessel
    cas220106.ves_vol = Meters3(4 / 3 * np.pi * build.vessel_ir**3)

    cas220106.C22010601 = to_m_usd(cas220106.ves_mat_cost * vacuum_system.ves_mfr)

    # Permissible force through one beam. Assuming tensile strength of steel of 420 MPa.
    beam_force_I = (
        vacuum_system.beam_cs_area * 420 * 1e6 / vacuum_system.factor_of_safety
    )
    # Total number of steel beams required to support vacuum vessel
    # TODO this is unused
    no_beams = (
        cas220106.mass_struct * 9.81 * vacuum_system.geometry_factor / beam_force_I
    )

    # COOLING 22.1.6.2
    # TODO currently always zero
    # scaled to system size, at system temperature
    cas220106.C22010602 = M_USD(0)

    # VACUUM PUMPING 22.1.6.3
    # Number of vacuum pumps required to pump the full vacuum in 1 second
    no_vpumps = int(cas220106.ves_vol / vacuum_system.vpump_cap)
    cas220106.C22010603 = to_m_usd(no_vpumps * vacuum_system.cost_pump)

    # ROUGHING PUMP 22.1.6.4
    # from STARFIRE, only 1 needed
    cas220106.C22010604 = M_USD(120000 * 2.85 / 1e6)

    cas220106.C220106 = M_USD(
        cas220106.C22010601
        + cas220106.C22010602
        + cas220106.C22010603
        + cas220106.C22010604
    )
    return cas220106
