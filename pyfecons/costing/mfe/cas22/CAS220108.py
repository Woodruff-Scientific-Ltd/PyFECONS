import numpy as np

from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.data import Data, TemplateProvider, CAS220108Divertor
from pyfecons.inputs import Inputs
from pyfecons.materials import Materials
from pyfecons.units import Meters, Meters3, Kilograms, M_USD

materials = Materials()


def cas_220108_divertor(inputs: Inputs, data: Data) -> TemplateProvider:
    OUT: CAS220108Divertor = data.cas220108
    assert isinstance(OUT, CAS220108Divertor)

    # 22.1.8 Divertor
    # Simple volumetric calculation based on reactor geometry, user input, and tungsten material
    # properties (see "materials" dictionary)
    # TODO confirm this formula
    OUT.divertor_maj_rad = Meters(data.cas220101.coil_ir - data.cas220101.axis_ir)
    OUT.divertor_min_rad = Meters(data.cas220101.firstwall_ir - data.cas220101.axis_ir)
    # TODO shouldn't 0.2 be a input?
    OUT.divertor_thickness_z = Meters(0.2)
    OUT.divertor_thickness_r = Meters(OUT.divertor_min_rad * 2)
    # TODO does this vary? Should it be an input?
    OUT.divertor_material = materials.W  # Tungsten

    # volume of the divertor based on TF coil radius
    OUT.divertor_vol = Meters3(((OUT.divertor_maj_rad + OUT.divertor_thickness_r) ** 2
                                - (OUT.divertor_maj_rad - OUT.divertor_thickness_r) ** 2)
                               * np.pi * OUT.divertor_thickness_z)
    OUT.divertor_mass = Kilograms(OUT.divertor_vol * OUT.divertor_material.rho)
    OUT.divertor_mat_cost = M_USD(OUT.divertor_mass * OUT.divertor_material.c_raw)
    OUT.divertor_cost = M_USD(OUT.divertor_mat_cost * OUT.divertor_material.m)
    OUT.C220108 = to_m_usd(OUT.divertor_cost)

    OUT.template_file = 'CAS220108_MFE.tex'
    OUT.replacements = {
        'C220108': round(OUT.C220108),
        # All of these are not in the templateo
        'divertorMajRad': round(OUT.divertor_maj_rad),
        'divertorMinRad': round(OUT.divertor_min_rad),
        'divertorThicknessZ': round(OUT.divertor_thickness_z),
        'divertorMaterial': OUT.divertor_material.name,
        'divertorVol': round(OUT.divertor_vol),
        'divertorMass': round(OUT.divertor_mass),
    }
    return OUT
