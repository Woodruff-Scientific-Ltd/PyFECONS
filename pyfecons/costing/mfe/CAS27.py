from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data, TemplateProvider
from pyfecons.enums import BlanketPrimaryCoolant

CAS_270000_TEX = 'CAS270000.tex'


def GenerateData(inputs: Inputs, data: Data, figures: dict) -> list[TemplateProvider]:
    # Cost Category 27 Special Materials
    OUT = data.cas27
    materials = inputs.materials

    # Select the coolant and calculate C_27_1
    # TODO where does 2130 come from?
    if inputs.blanket.primary_coolant == BlanketPrimaryCoolant.FLIBE:
        data.cas27.C271000 = 1000 * 2130 * materials.FliBe.c / 1e6
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.LEAD_LITHIUM_PBLI:
        # TODO should we pull these out into inputs?
        f_6Li = 0.1
        FPCPPFb = 0.9
        OUT.C271000 = M_USD((materials.Pb.c * FPCPPFb * data.cas220101.firstwall_vol * materials.FliBe.rho * 1000
                             + materials.Li.c * f_6Li * data.cas220101.firstwall_vol * materials.FliBe.rho * 1000
                             ) / 1e6)
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.LITHIUM_LI:
        OUT.C271000 = M_USD(1000 * 2130 * 50 / 1e6)
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.OTHER_EUTECTIC_SALT:
        OUT.C271000 = M_USD(1000 * 2130 * 50 / 1e6)
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.HELIUM:
        # TODO why 2.13 instead of 2130?
        OUT.C271000 = M_USD(1000 * 2.13 * 50 / 1e6)
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.DUAL_COOLANT_PBLI_AND_HE:
        # TODO why 2.13 instead of 2130?
        OUT.C271000 = M_USD(1000 * 2.13 * 50 / 1e6)
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.WATER:
        # TODO why 1000?
        OUT.C271000 = M_USD(1000 * 1000 * 1 / 1e6)

    # Additional calculations
    OUT.C274000 = M_USD(0.41 * 1.71)  # Other
    OUT.C275000 = M_USD(0.21 * 1.71)  # Reactor-building cover gas
    OUT.C270000 = M_USD(OUT.C271000 + OUT.C274000 + OUT.C275000)

    OUT.template_file = CAS_270000_TEX
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C270000': round(data.cas27.C270000)
    }
    return [OUT]
