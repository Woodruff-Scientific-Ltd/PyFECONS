from dataclasses import dataclass, field

from pyfecons.units import Percent


@dataclass
class NpvInput:
    # Financial discount rate (interest rate for short term loans)
    discount_rate: Percent = field(default=None)
