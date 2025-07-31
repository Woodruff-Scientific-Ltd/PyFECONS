from dataclasses import dataclass

from pyfecons.units import Ratio, Unknown


@dataclass
class Financial:
    # TODO what are these?
    a_c_98: Unknown = Unknown(115)
    a_power: Unknown = Unknown(1000)
    # Capital recovery factor see https://netl.doe.gov/projects/files/CostAndPerformanceBaselineForFossilEnergyPlantsVolume1BituminousCoalAndNaturalGasToElectricity_101422.pdf
    # TODO is the capital return or recovery factor? recovery is mentioned in mfe, return in ife
    capital_recovery_factor: Ratio = 0.09
