from dataclasses import dataclass

from pyfecons.units import Ratio, MJ


@dataclass
class Lasers:
    # Learning curve cost or time reduction between first and nth beamlet construction (default 5x)
    # TODO this is not used
    beamlet_learning_curve: Ratio = None
    # Beamlet learning curve coefficient b
    beamlet_learning_curve_coefficient_b: Ratio = None
    # NIF Laser energy for scaling (see
    # https://docs.google.com/spreadsheets/d/1sMNzOweYvZCR1BeCXR4IciHEikYyZ0a11XpnLshR6DU/edit#gid=1102621340
    # for justification of linear scaling)
    nif_laser_energy: MJ = None
