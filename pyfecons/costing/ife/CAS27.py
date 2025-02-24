from pyfecons.materials import Materials
from pyfecons.units import M_USD
from pyfecons.enums import BlanketPrimaryCoolant
from pyfecons.data import Data
from pyfecons.report import TemplateProvider
from pyfecons.inputs.all_inputs import AllInputs

materials = Materials()


def cas_27(inputs: AllInputs, data: Data) -> TemplateProvider:
    # Cost Category 27 Special Materials
    OUT = data.cas27
    blanket = inputs.blanket

    # Select the coolant and calculate C_27_1
    C_27_1 = 0
    if blanket.primary_coolant == BlanketPrimaryCoolant.FLIBE:
        C_27_1 = 1000 * 2130 * materials.FliBe.c / 1e6
    elif blanket.primary_coolant == BlanketPrimaryCoolant.LEAD_LITHIUM_PBLI:
        # TODO should we pull these out into inputs?
        f_6Li = 0.1
        FPCPPFb = 0.9
        C_27_1 = (
            materials.Pb.c
            * FPCPPFb
            * data.cas220101.firstwall_vol
            * materials.FliBe.rho
            * 1000
            + materials.Li.c
            * f_6Li
            * data.cas220101.firstwall_vol
            * materials.FliBe.rho
            * 1000
        ) / 1e6
    elif blanket.primary_coolant == BlanketPrimaryCoolant.LITHIUM_LI:
        C_27_1 = 1000 * 2130 * 50 / 1e6
    elif blanket.primary_coolant == BlanketPrimaryCoolant.OTHER_EUTECTIC_SALT:
        C_27_1 = 1000 * 2130 * 50 / 1e6
    elif blanket.primary_coolant == BlanketPrimaryCoolant.HELIUM:
        C_27_1 = 1000 * 2.13 * 50 / 1e6
    elif blanket.primary_coolant == BlanketPrimaryCoolant.DUAL_COOLANT_PBLI_AND_HE:
        C_27_1 = 1000 * 2.13 * 50 / 1e6
    elif blanket.primary_coolant == BlanketPrimaryCoolant.WATER:
        C_27_1 = 1000 * 1000 * 1 / 1e6

    # Additional calculations
    # TODO where do these constants come from?
    C_27_4 = 0.41 * 1.71  # Other
    C_27_5 = 0.21 * 1.71  # Reactor-building cover gas
    OUT.C270000 = M_USD(C_27_1 + C_27_4 + C_27_5)

    # TODO script references CAS270000_MIF_DT.tex, which template should we use?
    OUT.template_file = "CAS270000.tex"
    OUT.replacements = {"C270000": round(OUT.C270000)}
    return OUT
