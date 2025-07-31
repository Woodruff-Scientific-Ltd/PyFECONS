from io import BytesIO
from typing import Dict

import matplotlib

from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.costing.calculations.volume import (
    calc_volume_outer_hollow_torus,
    calc_volume_ring,
    calc_volume_sphere,
)
from pyfecons.costing.categories.cas220101 import CAS220101
from pyfecons.enums import BlanketFirstWall, BlanketType, ConfinementType, ReactorType
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.blanket import Blanket
from pyfecons.inputs.radial_build import RadialBuild
from pyfecons.materials import Material, Materials
from pyfecons.units import M_USD, Meters3

materials = Materials()


def cas_220101_reactor_equipment_costs(
    basic: Basic, radial_build: RadialBuild, blanket: Blanket
) -> CAS220101:
    # Cost Category 22.1.1: Reactor Equipment
    reactor_type = basic.reactor_type
    confinement_type = basic.confinement_type

    cas220101 = compute_reactor_equipment_costs(
        reactor_type, confinement_type, blanket, radial_build
    )
    return cas220101


def compute_reactor_equipment_costs(
    reactor_type: ReactorType,
    confinement_type: ConfinementType,
    blanket: Blanket,
    radial_build: RadialBuild,
) -> CAS220101:
    cas220101 = CAS220101()
    cas220101 = compute_inner_radii(reactor_type, radial_build, cas220101)
    cas220101 = compute_outer_radii(reactor_type, radial_build, cas220101)

    if (
        reactor_type == ReactorType.MFE
        and confinement_type == ConfinementType.SPHERICAL_TOKAMAK
    ):
        cas220101 = compute_volume_mfe_tokamak(radial_build, cas220101)
        # must be cylindrical in all cases
        cas220101.gap2_vol = calc_volume_ring(
            radial_build.axis_t,
            cas220101.gap2_ir,
            radial_build.gap2_t + cas220101.gap2_ir,
        )
        # Updated bioshield volume
        cas220101.bioshield_vol = calc_volume_ring(
            radial_build.axis_t,
            cas220101.bioshield_ir,
            radial_build.bioshield_t + cas220101.bioshield_ir,
        )
    elif (
        reactor_type == ReactorType.MFE
        and confinement_type == ConfinementType.MAGNETIC_MIRROR
    ):
        cas220101 = compute_volume_mfe_mirror(radial_build, cas220101)
    elif reactor_type == ReactorType.IFE:
        cas220101 = compute_volume_ife(cas220101)
    else:
        raise ValueError(f"Unsupported reactor type {reactor_type}")

    cas220101.C22010101 = compute_first_wall_costs(blanket, cas220101)
    cas220101.C22010102 = compute_blanket_costs(blanket, cas220101)

    # Total cost of blanket and first wall
    cas220101.C220101 = M_USD(cas220101.C22010101 + cas220101.C22010102)
    return cas220101


def compute_volume_mfe_tokamak(IN: RadialBuild, OUT: CAS220101) -> CAS220101:
    OUT.axis_vol = 0.0
    OUT.plasma_vol = Meters3(
        IN.elon * calc_volume_outer_hollow_torus(IN.axis_t, OUT.plasma_ir, IN.plasma_t)
        - OUT.axis_vol
    )
    OUT.vacuum_vol = Meters3(
        IN.elon * calc_volume_outer_hollow_torus(IN.axis_t, OUT.vacuum_ir, IN.vacuum_t)
        - sum([OUT.plasma_vol, OUT.axis_vol])
    )
    OUT.firstwall_vol = Meters3(
        IN.elon
        * calc_volume_outer_hollow_torus(IN.axis_t, OUT.firstwall_ir, IN.firstwall_t)
        - sum([OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol])
    )
    OUT.blanket1_vol = Meters3(
        IN.elon
        * calc_volume_outer_hollow_torus(IN.axis_t, OUT.blanket1_ir, IN.blanket1_t)
        - sum([OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol])
    )
    OUT.reflector_vol = Meters3(
        IN.elon
        * calc_volume_outer_hollow_torus(IN.axis_t, OUT.reflector_ir, IN.reflector_t)
        - sum(
            [
                OUT.blanket1_vol,
                OUT.firstwall_vol,
                OUT.vacuum_vol,
                OUT.plasma_vol,
                OUT.axis_vol,
            ]
        )
    )
    OUT.ht_shield_vol = Meters3(
        IN.elon
        * calc_volume_outer_hollow_torus(IN.axis_t, OUT.ht_shield_ir, IN.ht_shield_t)
        - sum(
            [
                OUT.reflector_vol,
                OUT.blanket1_vol,
                OUT.firstwall_vol,
                OUT.vacuum_vol,
                OUT.plasma_vol,
                OUT.axis_vol,
            ]
        )
    )
    OUT.structure_vol = Meters3(
        IN.elon
        * calc_volume_outer_hollow_torus(IN.axis_t, OUT.structure_ir, IN.structure_t)
        - sum(
            [
                OUT.ht_shield_vol,
                OUT.reflector_vol,
                OUT.blanket1_vol,
                OUT.firstwall_vol,
                OUT.vacuum_vol,
                OUT.plasma_vol,
                OUT.axis_vol,
            ]
        )
    )
    OUT.gap1_vol = Meters3(
        IN.elon * calc_volume_outer_hollow_torus(IN.axis_t, OUT.gap1_ir, IN.gap1_t)
        - sum(
            [
                OUT.structure_vol,
                OUT.ht_shield_vol,
                OUT.reflector_vol,
                OUT.blanket1_vol,
                OUT.firstwall_vol,
                OUT.vacuum_vol,
                OUT.plasma_vol,
                OUT.axis_vol,
            ]
        )
    )
    OUT.vessel_vol = Meters3(
        IN.elon * calc_volume_outer_hollow_torus(IN.axis_t, OUT.vessel_ir, IN.vessel_t)
        - sum(
            [
                OUT.gap1_vol,
                OUT.structure_vol,
                OUT.ht_shield_vol,
                OUT.reflector_vol,
                OUT.blanket1_vol,
                OUT.firstwall_vol,
                OUT.vacuum_vol,
                OUT.plasma_vol,
                OUT.axis_vol,
            ]
        )
    )
    OUT.lt_shield_vol = Meters3(
        IN.elon
        * calc_volume_outer_hollow_torus(IN.axis_t, OUT.lt_shield_ir, IN.lt_shield_t)
        - sum(
            [
                OUT.vessel_vol,
                OUT.gap1_vol,
                OUT.structure_vol,
                OUT.ht_shield_vol,
                OUT.reflector_vol,
                OUT.blanket1_vol,
                OUT.firstwall_vol,
                OUT.vacuum_vol,
                OUT.plasma_vol,
                OUT.axis_vol,
            ]
        )
    )
    OUT.coil_vol = Meters3(
        calc_volume_outer_hollow_torus(IN.axis_t, OUT.coil_ir, IN.coil_t) * 0.5
    )
    return OUT


def compute_volume_mfe_mirror(IN: RadialBuild, OUT: CAS220101) -> CAS220101:
    OUT.axis_vol = calc_volume_ring(IN.chamber_length, OUT.axis_ir, OUT.axis_or)
    OUT.plasma_vol = calc_volume_ring(IN.chamber_length, OUT.plasma_ir, OUT.plasma_or)
    OUT.vacuum_vol = calc_volume_ring(IN.chamber_length, OUT.vacuum_ir, OUT.vacuum_or)
    OUT.firstwall_vol = calc_volume_ring(
        IN.chamber_length, OUT.firstwall_ir, OUT.firstwall_or
    )
    OUT.blanket1_vol = calc_volume_ring(
        IN.chamber_length, OUT.blanket1_ir, OUT.blanket1_or
    )
    OUT.reflector_vol = calc_volume_ring(
        IN.chamber_length, OUT.reflector_ir, OUT.reflector_or
    )
    OUT.ht_shield_vol = calc_volume_ring(
        IN.chamber_length, OUT.ht_shield_ir, OUT.ht_shield_or
    )
    OUT.structure_vol = calc_volume_ring(
        IN.chamber_length, OUT.structure_ir, OUT.structure_or
    )
    OUT.gap1_vol = calc_volume_ring(IN.chamber_length, OUT.gap1_ir, OUT.gap1_or)
    OUT.vessel_vol = calc_volume_ring(IN.chamber_length, OUT.vessel_ir, OUT.vessel_or)
    # Moved lt_shield volume here
    OUT.lt_shield_vol = calc_volume_ring(
        IN.chamber_length, OUT.lt_shield_ir, OUT.lt_shield_or
    )
    # Updated coil volume calculation
    # TODO what's this constant: (9*0.779)/40
    OUT.coil_vol = (
        calc_volume_ring(IN.chamber_length, OUT.coil_ir, OUT.coil_or) * (9 * 0.779) / 40
    )
    OUT.gap2_vol = calc_volume_ring(IN.chamber_length, OUT.gap2_ir, OUT.gap2_or)
    # Updated bioshield volume
    OUT.bioshield_vol = calc_volume_ring(
        IN.chamber_length, OUT.bioshield_ir, OUT.bioshield_or
    )
    return OUT


def compute_volume_ife(OUT: CAS220101) -> CAS220101:
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
    return OUT


def compute_inner_radii(
    reactor_type: ReactorType, IN: RadialBuild, OUT: CAS220101
) -> CAS220101:
    # Inner radii
    OUT.axis_ir = IN.axis_t
    OUT.plasma_ir = OUT.axis_ir
    OUT.vacuum_ir = IN.plasma_t + OUT.plasma_ir
    OUT.firstwall_ir = IN.vacuum_t + OUT.vacuum_ir
    OUT.blanket1_ir = OUT.firstwall_ir + IN.firstwall_t
    OUT.reflector_ir = OUT.blanket1_ir + IN.blanket1_t
    OUT.ht_shield_ir = OUT.reflector_ir + IN.reflector_t
    OUT.structure_ir = OUT.ht_shield_ir + IN.ht_shield_t
    OUT.gap1_ir = OUT.structure_ir + IN.structure_t
    OUT.vessel_ir = OUT.gap1_ir + IN.gap1_t
    OUT.lt_shield_ir = OUT.vessel_ir + IN.vessel_t  # Adjusted lt_shield inner radius

    if reactor_type == ReactorType.MFE:
        OUT.coil_ir = OUT.lt_shield_ir + IN.lt_shield_t  # Updated coil_ir calculation
        OUT.gap2_ir = OUT.coil_ir + IN.coil_t
    else:
        OUT.gap2_ir = (
            OUT.lt_shield_ir + IN.lt_shield_t
        )  # Adjusted gap2 inner radius directly after lt_shield

    OUT.bioshield_ir = OUT.gap2_ir + IN.gap2_t  # Adjusted bioshield inner radius
    return OUT


def compute_outer_radii(
    reactor_type: ReactorType, IN: RadialBuild, OUT: CAS220101
) -> CAS220101:
    # Outer radii
    OUT.axis_or = OUT.axis_ir + IN.axis_t
    OUT.plasma_or = OUT.plasma_ir + IN.plasma_t
    OUT.vacuum_or = OUT.vacuum_ir + IN.vacuum_t
    OUT.firstwall_or = OUT.firstwall_ir + IN.firstwall_t
    OUT.blanket1_or = OUT.blanket1_ir + IN.blanket1_t
    OUT.reflector_or = OUT.reflector_ir + IN.reflector_t
    OUT.ht_shield_or = OUT.ht_shield_ir + IN.ht_shield_t
    OUT.structure_or = OUT.structure_ir + IN.structure_t
    OUT.gap1_or = OUT.gap1_ir + IN.gap1_t
    OUT.vessel_or = OUT.vessel_ir + IN.vessel_t
    OUT.lt_shield_or = (
        OUT.lt_shield_ir + IN.lt_shield_t
    )  # Adjusted lt_shield outer radius

    if reactor_type == ReactorType.MFE:
        OUT.coil_or = OUT.coil_ir + IN.coil_t  # Updated coil_or calculation

    OUT.gap2_or = (
        OUT.gap2_ir + IN.gap2_t
    )  # Adjusted gap2 outer radius directly after lt_shield
    OUT.bioshield_or = (
        OUT.bioshield_ir + IN.bioshield_t
    )  # Adjusted bioshield outer radius
    return OUT


def compute_first_wall_costs(blanket: Blanket, OUT: CAS220101) -> M_USD:
    # First wall
    if blanket.first_wall == BlanketFirstWall.TUNGSTEN:
        return compute_material_cost(OUT.firstwall_vol, materials.W)
    elif blanket.first_wall == BlanketFirstWall.LIQUID_LITHIUM:
        return compute_material_cost(OUT.firstwall_vol, materials.Li)
    elif blanket.first_wall == BlanketFirstWall.BERYLLIUM:
        return compute_material_cost(OUT.firstwall_vol, materials.Be)
    elif blanket.first_wall == BlanketFirstWall.FLIBE:
        return compute_material_cost(OUT.firstwall_vol, materials.FliBe)
    raise f"Unknown first wall type {blanket.first_wall}"


def compute_blanket_costs(blanket: Blanket, OUT: CAS220101) -> M_USD:
    # Blanket
    if blanket.blanket_type == BlanketType.FLOWING_LIQUID_FIRST_WALL:
        return compute_material_cost(OUT.blanket1_vol, materials.Li)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER:
        return compute_material_cost(OUT.blanket1_vol, materials.Li)
    elif (
        blanket.blanket_type
        == BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI4SIO4
    ):
        return compute_material_cost(OUT.blanket1_vol, materials.Li4SiO4)
    elif (
        blanket.blanket_type
        == BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3
    ):
        return compute_material_cost(OUT.blanket1_vol, materials.Li2TiO3)
    elif (
        blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_NO_BREEDER_ANEUTRONIC_FUEL
    ):
        return M_USD(0)
    raise f"Unknown blanket type {blanket.blanket_type}"


def compute_material_cost(volume: Meters3, material: Material) -> M_USD:
    return to_m_usd(volume * material.rho * material.c_raw * material.m)
