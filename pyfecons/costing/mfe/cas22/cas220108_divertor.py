import numpy as np

from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.costing.categories.cas220101 import CAS220101
from pyfecons.costing.categories.cas220108_divertor import CAS220108Divertor
from pyfecons.materials import Materials
from pyfecons.units import Meters, Meters3, Kilograms, M_USD, Ratio

materials = Materials()


def cas_220108_divertor_costs(cas220101: CAS220101) -> CAS220108Divertor:
    cas220108: CAS220108Divertor = CAS220108Divertor()

    # 22.1.8 Divertor
    # Simple volumetric calculation based on reactor geometry, user input, and tungsten material
    # properties (see "materials" dictionary)
    # TODO confirm this formula
    cas220108.divertor_maj_rad = Meters(cas220101.coil_ir - cas220101.axis_ir)
    cas220108.divertor_min_rad = Meters(cas220101.firstwall_ir - cas220101.axis_ir)
    # TODO these should probably be inputs
    cas220108.divertor_thickness_z = Meters(0.5)
    cas220108.divertor_complexity_factor = Ratio(3)
    cas220108.divertor_vol_frac = Ratio(0.2)
    cas220108.divertor_thickness_r = Meters(cas220108.divertor_min_rad * 2)
    cas220108.divertor_material = materials.W

    cas220108.divertor_vol = Meters3(
        (
            (cas220108.divertor_maj_rad + cas220108.divertor_thickness_r) ** 2
            - (cas220108.divertor_maj_rad - cas220108.divertor_thickness_r) ** 2
        )
        * np.pi
        * cas220108.divertor_thickness_z
        * cas220108.divertor_vol_frac
    )
    cas220108.divertor_mass = Kilograms(
        cas220108.divertor_vol * cas220108.divertor_material.rho
    )
    cas220108.divertor_mat_cost = M_USD(
        cas220108.divertor_mass * cas220108.divertor_material.c_raw
    )
    cas220108.divertor_cost = M_USD(
        cas220108.divertor_mat_cost
        * cas220108.divertor_material.m
        * cas220108.divertor_complexity_factor
    )
    cas220108.C220108 = to_m_usd(cas220108.divertor_cost)
    return cas220108
