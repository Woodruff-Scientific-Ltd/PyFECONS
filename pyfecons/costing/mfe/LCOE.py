from pyfecons import M_USD
from pyfecons.inputs import Inputs
from pyfecons.data import Data


def GenerateData(inputs: Inputs, data: Data, figures: dict):
    # LCOE = _____ Cost of Electricity
    OUT = data.lcoe
    OUT.C1000000 = M_USD(
        (data.cas90.C900000 * 1e6 + (data.cas70.C700000 * 1e6 + data.cas80.C800000 * 1e6)
         * (1 + inputs.basic.yearly_inflation) ** inputs.basic.plant_lifetime)
        / (8760 * data.power_table.p_net * (float(inputs.basic.n_mod) * inputs.basic.plant_availability)))
    OUT.C2000000 = M_USD(OUT.C1000000 / 10)
