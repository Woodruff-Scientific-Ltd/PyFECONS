from pyfecons.costing.calculations.cas22.cas220101_reactor_equipment import compute_inner_radii, compute_outer_radii, \
    compute_first_wall_costs, compute_blanket_costs, plot_radial_build, compute_220101_replacements
from pyfecons.costing.calculations.volume import calc_volume_sphere
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs
from pyfecons.units import M_USD


def cas_220101_reactor_equipment(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.1: Reactor Equipment
    IN  = inputs.radial_build
    OUT = data.cas220101
    blanket = inputs.blanket
    materials = inputs.materials
    reactor_type = inputs.basic.reactor_type

    compute_inner_radii(reactor_type, IN, OUT)
    compute_outer_radii(reactor_type, IN, OUT)
    compute_volume(OUT)

    OUT.C22010101 = compute_first_wall_costs(blanket, materials, OUT)
    OUT.C22010102 = compute_blanket_costs(blanket, materials, OUT)
    OUT.C220101 = M_USD(OUT.C22010101 + OUT.C22010102)  # Total cost of blanket and first wall

    OUT.figures['Figures/radial_build.pdf'] = plot_radial_build(reactor_type, IN)
    OUT.template_file = 'CAS220101_IFE_DT.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = compute_220101_replacements(reactor_type, blanket, IN, OUT)
    return OUT


def compute_volume(OUT) -> None:
    OUT.axis_vol = calc_volume_sphere(OUT.axis_ir, OUT.axis_or)
    OUT.plasma_vol = calc_volume_sphere(OUT.plasma_ir, OUT.plasma_or)
    OUT.vacuum_vol = calc_volume_sphere(OUT.vacuum_ir, OUT.vacuum_or)
    OUT.firstwall_vol = calc_volume_sphere(OUT.firstwall_ir, OUT.firstwall_or)
    OUT.blanket1_vol = calc_volume_sphere(OUT.blanket1_ir, OUT.blanket1_or)
    OUT.reflector_vol = calc_volume_sphere(OUT.reflector_ir, OUT.reflector_or)
    OUT.ht_shield_vol = calc_volume_sphere(OUT.ht_shield_ir, OUT.ht_shield_or)
    OUT.structure_vol = calc_volume_sphere(OUT.structure_ir, OUT.structure_or)
    OUT.gap1_vol = calc_volume_sphere(OUT.gap1_ir, OUT.gap1_or)
    OUT.vessel_vol = calc_volume_sphere(OUT.vessel_ir, OUT.vessel_or)
    OUT.lt_shield_vol = calc_volume_sphere(OUT.lt_shield_ir, OUT.lt_shield_or)
    OUT.gap2_vol = calc_volume_sphere(OUT.gap2_ir, OUT.gap2_or)
    OUT.bioshield_vol = calc_volume_sphere(OUT.bioshield_ir, OUT.bioshield_or)