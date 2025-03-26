from dataclasses import dataclass, field

from pyfecons.units import Ratio


@dataclass
class TargetFactory:
    learning_credit: Ratio = field(default=None)
