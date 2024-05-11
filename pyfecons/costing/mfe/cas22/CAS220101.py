import numpy as np

from pyfecons.costing.calculations.cas22.cas220101_reactor_equipment import compute_outer_radii, compute_inner_radii, \
    compute_first_wall_costs, compute_blanket_costs, plot_radial_build, compute_220101_replacements
from pyfecons.costing.calculations.volume import calc_volume_ring
from pyfecons.data import Data, TemplateProvider, CAS220101
from pyfecons.inputs import Inputs, RadialBuild
from pyfecons.units import Meters3, M_USD


def cas_220101_reactor_equipment(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.1: Reactor Equipment
    radial_build = inputs.radial_build
    IN = radial_build
    OUT = data.cas220101
    reactor_type = inputs.basic.reactor_type
    blanket = inputs.blanket
    materials = inputs.materials

    compute_inner_radii(reactor_type, IN, OUT)
    compute_outer_radii(reactor_type, IN, OUT)
    compute_volume(IN, OUT)

    # must be cylindrical in all cases
    OUT.gap2_vol = calc_volume_ring(IN.axis_t, IN.gap2_t + OUT.gap2_ir, OUT.gap2_ir)
    # Updated bioshield volume
    OUT.bioshield_vol = calc_volume_ring(IN.axis_t, IN.bioshield_t + OUT.bioshield_ir, OUT.bioshield_ir)

    OUT.C22010101 = compute_first_wall_costs(blanket, materials, OUT)
    OUT.C22010102 = compute_blanket_costs(blanket, materials, OUT)

    # Total cost of blanket and first wall
    OUT.C220101 = M_USD(OUT.C22010101 + OUT.C22010102)

    OUT.figures['Figures/radial_build.pdf'] = plot_radial_build(reactor_type, IN)

    OUT.template_file = 'CAS220101_MFE_DT.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = compute_220101_replacements(reactor_type, blanket, IN, OUT)
    return OUT


def compute_volume(IN: RadialBuild, OUT: CAS220101) -> None:
    OUT.axis_vol = 0.0
    OUT.plasma_vol = Meters3(IN.elon * calc_volume_torus(IN.axis_t, OUT.plasma_ir, IN.plasma_t) - OUT.axis_vol)
    OUT.vacuum_vol = Meters3(IN.elon * calc_volume_torus(IN.axis_t, OUT.vacuum_ir, IN.vacuum_t)
                             - sum([OUT.plasma_vol, OUT.axis_vol]))
    OUT.firstwall_vol = Meters3(IN.elon * calc_volume_torus(IN.axis_t, OUT.firstwall_ir, IN.firstwall_t)
                                - sum([OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.blanket1_vol = Meters3(IN.elon * calc_volume_torus(IN.axis_t, OUT.blanket1_ir, IN.blanket1_t)
                               - sum([OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.reflector_vol = Meters3(IN.elon * calc_volume_torus(IN.axis_t, OUT.reflector_ir, IN.reflector_t)
                                - sum([OUT.blanket1_vol, OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol,
                                       OUT.axis_vol]))
    OUT.ht_shield_vol = Meters3(IN.elon * calc_volume_torus(IN.axis_t, OUT.ht_shield_ir, IN.ht_shield_t)
                                - sum([OUT.reflector_vol, OUT.blanket1_vol, OUT.firstwall_vol,
                                       OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.structure_vol = Meters3(IN.elon * calc_volume_torus(IN.axis_t, OUT.structure_ir, IN.structure_t)
                                - sum([OUT.ht_shield_vol, OUT.reflector_vol, OUT.blanket1_vol, OUT.firstwall_vol,
                                       OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.gap1_vol = Meters3(IN.elon * calc_volume_torus(IN.axis_t, OUT.gap1_ir, IN.gap1_t)
                           - sum([OUT.structure_vol, OUT.ht_shield_vol, OUT.reflector_vol, OUT.blanket1_vol,
                                  OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.vessel_vol = Meters3(IN.elon * calc_volume_torus(IN.axis_t, OUT.vessel_ir, IN.vessel_t)
                             - sum([OUT.gap1_vol, OUT.structure_vol, OUT.ht_shield_vol, OUT.reflector_vol,
                                    OUT.blanket1_vol, OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.lt_shield_vol = Meters3(IN.elon * calc_volume_torus(IN.axis_t, OUT.lt_shield_ir, IN.lt_shield_t)
                                - sum([OUT.vessel_vol, OUT.gap1_vol, OUT.structure_vol, OUT.ht_shield_vol,
                                       OUT.reflector_vol, OUT.blanket1_vol, OUT.firstwall_vol, OUT.vacuum_vol,
                                       OUT.plasma_vol, OUT.axis_vol]))
    OUT.coil_vol = Meters3(calc_volume_torus(IN.axis_t, OUT.coil_ir, IN.coil_t) * 0.5)


def calc_volume_torus(radius: float, inner: float, outer: float):
    return Meters3(2 * np.pi * radius * np.pi * (inner + outer) ** 2)
