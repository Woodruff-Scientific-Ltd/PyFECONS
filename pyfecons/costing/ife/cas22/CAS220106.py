import numpy as np

from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.materials import Materials
from pyfecons.units import Meters3, M_USD

materials = Materials()


def cas_220106_vacuum_system(inputs: Inputs, data: Data) -> TemplateProvider:
    # 22.1.6 Vacuum system
    # 22.1.6.1 Vacuum Vessel
    OUT = data.cas220106
    build = data.cas220101
    IN = inputs.vacuum_system

    # Calculate mass and cost
    material_volume = build.vessel_vol
    mass_struct = material_volume * materials.SS316.rho
    # vessel material cost
    ves_mat_cost = materials.SS316.c_raw * mass_struct
    # internal volume of the vacuum vessel
    ves_vol = Meters3(4 / 3 * np.pi * build.vessel_ir**3)

    OUT.C22010601 = to_m_usd(ves_mat_cost * IN.ves_mfr)

    # Permissible force through one beam. Assuming tensile strength of steel of 420 MPa.
    beam_force_I = IN.beam_cs_area * 420 * 1e6 / IN.factor_of_safety
    # Total number of steel beams required to support vacuum vessel
    # TODO this is unused
    no_beams = mass_struct * 9.81 * IN.geometry_factor / beam_force_I

    # COOLING 22.1.6.2
    # TODO currently always zero
    # scaled to system size, at system temperature
    OUT.C22010602 = M_USD(0)

    # VACUUM PUMPING 22.1.6.3
    # Number of vacuum pumps required to pump the full vacuum in 1 second
    no_vpumps = int(ves_vol / IN.vpump_cap)
    OUT.C22010603 = to_m_usd(no_vpumps * IN.cost_pump)

    # ROUGHING PUMP 22.1.6.4
    # from STARFIRE, only 1 needed
    OUT.C22010604 = M_USD(120000 * 2.85 / 1e6)

    OUT.C220106 = M_USD(OUT.C22010601 + OUT.C22010602 + OUT.C22010603 + OUT.C22010604)
    OUT.template_file = "CAS220106_IFE.tex"
    OUT.replacements = {
        "C22010601": round(OUT.C22010601),
        "C22010602": round(OUT.C22010602),
        "C22010603": round(OUT.C22010603),
        "C22010604": round(OUT.C22010604, 2),
        "C22010600": round(OUT.C220106),
        "vesvol": round(ves_vol),
        "materialvolume": round(material_volume),
        "massstruct": round(mass_struct / 1e3),
        "vesmatcost": round(ves_mat_cost / 1e6, 1),
        "vesmfr": round(IN.ves_mfr),
    }
    return OUT
