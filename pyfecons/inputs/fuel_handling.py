import math
from dataclasses import dataclass

from pyfecons.units import Ratio


@dataclass
class FuelHandling:
    learning_curve_credit: Ratio
    learning_tenth_of_a_kind: Ratio = None

    def __post_init__(self):
        if self.learning_tenth_of_a_kind is None:
            self.learning_tenth_of_a_kind = Ratio(
                10 ** (math.log10(self.learning_curve_credit) / math.log10(2))
            )
