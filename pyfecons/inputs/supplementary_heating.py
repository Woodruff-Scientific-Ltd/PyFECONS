from dataclasses import dataclass, field

from pyfecons.inputs.heating_ref import HeatingRef
from pyfecons.units import MW


@dataclass
class SupplementaryHeating:
    # see pg 90 https://cer.ucsd.edu/_files/publications/UCSD-CER-13-01.pdf
    nbi_power: MW = MW(50)
    icrf_power: MW = MW(0)
    aries_at: HeatingRef = field(
        default_factory=lambda: HeatingRef(
            "ARIES-AT", "ICRF/LH", MW(37.441), 1.67, 2.3881
        )
    )
    aries_i_a: HeatingRef = field(
        default_factory=lambda: HeatingRef(
            "ARIES-I", "ICRF/LH", MW(96.707), 1.87, 2.6741
        )
    )
    aries_i_b: HeatingRef = field(
        default_factory=lambda: HeatingRef(
            "ARIES-I'", "ICRF/LH", MW(202.5), 1.96, 2.8028
        )
    )
    aries_rs: HeatingRef = field(
        default_factory=lambda: HeatingRef(
            "ARIES-RS", "ICRF/LH/HFFW", MW(80.773), 3.09, 4.4187
        )
    )
    aries_iv: HeatingRef = field(
        default_factory=lambda: HeatingRef("ARIES-IV", "ICRF/LH", MW(68), 4.35, 6.2205)
    )
    aries_ii: HeatingRef = field(
        default_factory=lambda: HeatingRef(
            "ARIES-II", "ICRF/LH", MW(66.1), 4.47, 6.3921
        )
    )
    # TODO why are there two ARIES-III?
    aries_iii_a: HeatingRef = field(
        default_factory=lambda: HeatingRef("ARIES-III'", "NBI", MW(163.2), 4.93, 7.0499)
    )
    aries_iii_b: HeatingRef = field(
        default_factory=lambda: HeatingRef("ARIES-III", "NBI", MW(172), 4.95, 7.0785)
    )
    iter: HeatingRef = field(
        default_factory=lambda: HeatingRef("ITER", "ICRF", MW(5.5), None, 7.865)
    )
    average: HeatingRef = field(
        default_factory=lambda: HeatingRef(
            "Average", None, MW(110.840125), 3.643333333, 5.209966667
        )
    )
    average_icrf: HeatingRef = field(
        default_factory=lambda: HeatingRef(
            "Average (ICRF)", None, MW(91.92016667), 2.901666667, 4.149383333
        )
    )
    average_nbi: HeatingRef = field(
        default_factory=lambda: HeatingRef(
            "Average (NBI)", None, MW(167.6), 4.94, 7.0642
        )
    )

    def heating_refs(self):
        return [
            self.aries_at,
            self.aries_i_a,
            self.aries_i_b,
            self.aries_rs,
            self.aries_iv,
            self.aries_ii,
            self.aries_iii_a,
            self.aries_iii_b,
            self.iter,
            self.average,
            self.average_icrf,
            self.average_nbi,
        ]
