from pyfecons.inputs import Inputs
from pyfecons.data import Data
from pyfecons.enums import BlanketPrimaryCoolant


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    # Cost Category 27 Special Materials

    # "Assuming the values for c_Flibe, c_Pb, c_Li, and MLM are defined elsewhere in your code"
    #   - the original workbook said this
    # I couldn't find these defined anywhere in the workbook - must ask Alex

    materials = inputs.materials
    # TODO - figure out what the actual value is here
    MLM = 1
    # Select the coolant and calculate C_27_1
    if inputs.blanket.primary_coolant == BlanketPrimaryCoolant.FLIBE:
        data.cas27.C271000 = 1000 * 2130 * materials.Flibe.c / 1e6
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.LEAD_LITHIUM_PBLI:
        f_6Li = 0.1
        FPCPPFb = 0.9
        data.cas27.C271000 = (materials.Pb.c * FPCPPFb * MLM * 1000 + materials.Li.c * f_6Li * MLM * 1000) / 1e6
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.LITHIUM_LI:
        data.cas27.C271000 = 1000 * 2130 * 50 / 1e6
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.OTHER_EUTECTIC_SALT:
        data.cas27.C271000 = 1000 * 2130 * 50 / 1e6
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.HELIUM:
        data.cas27.C271000 = 1000 * 2.13 * 50 / 1e6
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.DUAL_COOLANT_PBLI_AND_HE:
        data.cas27.C271000 = 1000 * 2.13 * 50 / 1e6
    elif inputs.blanket.primary_coolant == BlanketPrimaryCoolant.WATER:
        data.cas27.C271000 = 1000 * 1000 * 1 / 1e6

    # Additional calculations
    data.cas27.C274000 = 0.41 * 1.71  # Other
    data.cas27.C275000 = 0.21 * 1.71  # Reactor-building cover gas
    data.cas27.C270000 = round(data.cas27.C271000 + data.cas27.C274000 + data.cas27.C275000, 1)
