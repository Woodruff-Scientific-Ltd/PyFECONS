from dataclasses import dataclass
from pyfecons.materials import Material
from pyfecons.report import ReportSection
from pyfecons.units import M_USD, Meters, Ratio, Meters3, Kilograms


@dataclass
class CAS220108Divertor(ReportSection):
    # 22.1.8 Divertor
    C220108: M_USD = None
    divertor_maj_rad: Meters = None
    divertor_min_rad: Meters = None
    divertor_thickness_z: Meters = None
    divertor_complexity_factor: Ratio = (
        None  # arbitrary measure of how complicated the divertor design is
    )
    divertor_vol_frac: Ratio = None  # fraction of volume of divertor that is material
    divertor_thickness_r: Meters = None
    divertor_material: Material = None
    divertor_vol: Meters3 = None  # volume of the divertor based on TF coil radius
    divertor_mass: Kilograms = None
    divertor_mat_cost: M_USD = None
    divertor_cost: M_USD = None
