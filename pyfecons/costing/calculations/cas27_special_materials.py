from pyfecons.costing.categories.cas220101 import CAS220101
from pyfecons.costing.categories.cas270000 import CAS27
from pyfecons.enums import BlanketPrimaryCoolant
from pyfecons.inputs.blanket import Blanket
from pyfecons.materials import Materials
from pyfecons.units import M_USD

materials = Materials()


def cas27_special_materials_costs(blanket: Blanket, cas220101: CAS220101) -> CAS27:
    # Cost Category 27 Special Materials
    cas27 = CAS27()

    # Select the coolant and calculate C_27_1
    # TODO where does 2130 come from?
    if blanket.primary_coolant == BlanketPrimaryCoolant.FLIBE:
        cas27.C271000 = 1000 * 2130 * materials.FliBe.c / 1e6
    elif blanket.primary_coolant == BlanketPrimaryCoolant.LEAD_LITHIUM_PBLI:
        # TODO should we pull these out into inputs?
        f_6Li = 0.1
        FPCPPFb = 0.9
        cas27.C271000 = M_USD(
            (
                materials.Pb.c
                * FPCPPFb
                * cas220101.firstwall_vol
                * materials.FliBe.rho
                * 1000
                + materials.Li.c
                * f_6Li
                * cas220101.firstwall_vol
                * materials.FliBe.rho
                * 1000
            )
            / 1e6
        )
    elif blanket.primary_coolant == BlanketPrimaryCoolant.LITHIUM_LI:
        cas27.C271000 = M_USD(1000 * 2130 * 50 / 1e6)
    elif blanket.primary_coolant == BlanketPrimaryCoolant.OTHER_EUTECTIC_SALT:
        cas27.C271000 = M_USD(1000 * 2130 * 50 / 1e6)
    elif blanket.primary_coolant == BlanketPrimaryCoolant.HELIUM:
        # TODO why 2.13 instead of 2130?
        cas27.C271000 = M_USD(1000 * 2.13 * 50 / 1e6)
    elif blanket.primary_coolant == BlanketPrimaryCoolant.DUAL_COOLANT_PBLI_AND_HE:
        # TODO why 2.13 instead of 2130?
        cas27.C271000 = M_USD(1000 * 2.13 * 50 / 1e6)
    elif blanket.primary_coolant == BlanketPrimaryCoolant.WATER:
        # TODO why 1000?
        cas27.C271000 = M_USD(1000 * 1000 * 1 / 1e6)

    # Additional calculations
    cas27.C274000 = M_USD(0.41 * 1.71)  # Other
    cas27.C275000 = M_USD(0.21 * 1.71)  # Reactor-building cover gas
    cas27.C270000 = M_USD(cas27.C271000 + cas27.C274000 + cas27.C275000)

    cas27.template_file = "CAS270000.tex"
    cas27.replacements = {"C270000": round(cas27.C270000)}
    return cas27
