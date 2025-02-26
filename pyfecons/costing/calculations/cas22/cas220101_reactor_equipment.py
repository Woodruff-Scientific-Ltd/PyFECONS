import matplotlib

from io import BytesIO
from typing import Dict
from matplotlib import pyplot as plt
from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.costing.calculations.volume import (
    calc_volume_ring,
    calc_volume_outer_hollow_torus,
    calc_volume_sphere,
)
from pyfecons.data import CAS220101
from pyfecons.enums import ReactorType, BlanketFirstWall, BlanketType, ConfinementType
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.blanket import Blanket
from pyfecons.inputs.radial_build import RadialBuild
from pyfecons.materials import Materials, Material
from pyfecons.units import M_USD, Meters3

materials = Materials()

matplotlib.use("Agg")


def cas_220101_reactor_equipment_costs(
    basic: Basic, radial_build: RadialBuild, blanket: Blanket
) -> CAS220101:
    # Cost Category 22.1.1: Reactor Equipment
    reactor_type = basic.reactor_type
    confinement_type = basic.confinement_type

    cas220101 = compute_reactor_equipment_costs(
        reactor_type, confinement_type, blanket, radial_build
    )
    cas220101.figures["Figures/radial_build.pdf"] = plot_radial_build(
        reactor_type, radial_build
    )

    cas220101.template_file = get_template_file(reactor_type)
    cas220101.replacements = compute_220101_replacements(
        reactor_type, blanket, radial_build, cas220101
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


def plot_radial_build(reactor_type: ReactorType, radial_build: RadialBuild) -> bytes:
    """
    PLOTTING RADIAL BUILD
    """
    IN = radial_build

    # The names of the sections
    # Updated order of the sections
    sections = [
        "Plasma",
        "Vacuum",
        "First Wall",
        "Blanket",
        "Reflector",
        "HT Shield",
        "Structure",
        "Gap",
        "Vessel",
        "LT Shield",
        *(["Coil"] if reactor_type == ReactorType.MFE else []),  # include only for MFE
        "Gap",
        "Bioshield",
    ]

    # The thickness of each section (for stacked bar plot)
    thickness = [
        IN.plasma_t,
        IN.vacuum_t,
        IN.firstwall_t,
        IN.blanket1_t,
        IN.reflector_t,
        IN.ht_shield_t,
        IN.structure_t,
        IN.gap1_t,
        IN.vessel_t,
        IN.lt_shield_t,
        *(
            [IN.coil_t] if reactor_type == ReactorType.MFE else []
        ),  # include only for MFE
        IN.gap2_t,
        IN.bioshield_t,
    ]

    # Updated colors for each section
    colors = [
        "purple",
        "black",
        "lightblue",
        "darkblue",
        "blue",
        "cornflowerblue",
        "coral",
        "lightgray",
        "orange",
        "slateblue",
        *(["green"] if reactor_type == ReactorType.MFE else []),  # include only for MFE
        "lightgray",
        "darkorange",
    ]

    # Plotting the stacked bar graph
    fig, ax = plt.subplots(
        figsize=(18, 3.5)
    )  # Adjust the figsize to get the desired aspect ratio

    # Adding each section to the bar plot
    left = 0  # Initialize left at 0
    for i, (section, thk) in enumerate(zip(sections, thickness)):
        ax.barh(
            "Thickness",
            thk,
            left=left,
            color=colors[i],
            edgecolor="white",
            label=section,
        )
        left += thk  # Increment left by the thickness of the current section

    # Setting labels and title
    ax.set_xlabel("Radius (m)")

    # Creating the legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    # Show grid for the x-axis
    ax.xaxis.grid(True)

    # Show the plot
    plt.tight_layout()

    # save figure
    figure_data = BytesIO()
    fig.savefig(figure_data, format="pdf", bbox_inches="tight")
    figure_data.seek(0)
    plt.close(fig)
    return figure_data.read()


def get_template_file(reactor_type: ReactorType):
    if reactor_type == ReactorType.MFE:
        return "CAS220101_MFE_DT.tex"
    if reactor_type == ReactorType.IFE:
        return "CAS220101_IFE_DT.tex"
    raise ValueError(f"Unsupported reactor type {reactor_type}")


def compute_220101_replacements(
    reactor_type: ReactorType, blanket: Blanket, IN: RadialBuild, OUT: CAS220101
) -> Dict[str, str]:
    rounding = 2
    return {
        "C22010100": str(OUT.C220101),
        "C22010101": str(OUT.C22010101),
        "C22010102": str(OUT.C22010102),
        "primaryC": blanket.primary_coolant.display_name,
        "secondaryC": blanket.secondary_coolant.display_name,
        "neutronM": blanket.neutron_multiplier.display_name,
        "structure1": blanket.structure.display_name,
        "firstW": blanket.first_wall.display_name,
        "TH01": round(IN.plasma_t, rounding),
        "TH02": round(IN.vacuum_t, rounding),
        "TH03": round(IN.firstwall_t, rounding),
        "TH04": round(IN.blanket1_t, rounding),
        "TH05": round(IN.structure_t, rounding),
        "TH06": round(IN.reflector_t, rounding),
        "TH07": round(IN.gap1_t, rounding),
        "TH08": round(IN.vessel_t, rounding),
        "TH09": round(IN.ht_shield_t, rounding),
        "TH10": round(IN.lt_shield_t, rounding),
        **(
            {"TH11": round(IN.coil_t, rounding)}
            if reactor_type == ReactorType.MFE
            else {}
        ),
        "TH12": round(IN.axis_t, rounding),
        "TH13": round(IN.gap2_t, rounding),
        "TH14": round(IN.bioshield_t, rounding),
        "RAD1I": round(OUT.plasma_ir, rounding),
        "RAD2I": round(OUT.vacuum_ir, rounding),
        "RAD3I": round(OUT.firstwall_ir, rounding),
        "RAD4I": round(OUT.blanket1_ir, rounding),
        "RAD5I": round(OUT.structure_ir, rounding),
        "RAD6I": round(OUT.reflector_ir, rounding),
        "RAD7I": round(OUT.gap1_ir, rounding),
        "RAD8I": round(OUT.vessel_ir, rounding),
        "RAD9I": round(OUT.ht_shield_ir, rounding),
        "RAD10I": round(OUT.lt_shield_ir, rounding),
        **(
            {"RAD11I": round(OUT.coil_ir, rounding)}
            if reactor_type == ReactorType.MFE
            else {}
        ),
        "RAD12I": round(OUT.axis_ir, rounding),
        "RAD13I": round(OUT.gap2_ir, rounding),
        "RAD14I": round(OUT.bioshield_ir, rounding),
        "RAD1O": round(OUT.plasma_or, rounding),
        "RAD2O": round(OUT.vacuum_or, rounding),
        "RAD3O": round(OUT.firstwall_or, rounding),
        "RAD4O": round(OUT.blanket1_or, rounding),
        "RAD5O": round(OUT.structure_or, rounding),
        "RAD6O": round(OUT.reflector_or, rounding),
        "RAD7O": round(OUT.gap1_or, rounding),
        "RAD8O": round(OUT.vessel_or, rounding),
        "RAD9O": round(OUT.ht_shield_or, rounding),
        "RAD10O": round(OUT.lt_shield_or, rounding),
        **(
            {"RAD11O": round(OUT.coil_or, rounding)}
            if reactor_type == ReactorType.MFE
            else {}
        ),
        "RAD12O": round(OUT.axis_or, rounding),
        "RAD13O": round(OUT.gap2_or, rounding),
        "RAD14O": round(OUT.bioshield_or, rounding),
        "VOL01": round(OUT.plasma_vol, rounding),
        "VOL02": round(OUT.vacuum_vol, rounding),
        "VOL03": round(OUT.firstwall_vol, rounding),
        "VOL04": round(OUT.blanket1_vol, rounding),
        "VOL05": round(OUT.structure_vol, rounding),
        "VOL06": round(OUT.reflector_vol, rounding),
        "VOL07": round(OUT.gap1_vol, rounding),
        "VOL08": round(OUT.vessel_vol, rounding),
        "VOL09": round(OUT.ht_shield_vol, rounding),
        "VOL10": round(OUT.lt_shield_vol, rounding),
        **(
            {"VOL11": round(OUT.coil_vol, rounding)}
            if reactor_type == ReactorType.MFE
            else {}
        ),
        "VOL12": round(OUT.axis_vol, rounding),
        "VOL13": round(OUT.gap2_vol, rounding),
        "VOL14": round(OUT.bioshield_vol, rounding),
    }
