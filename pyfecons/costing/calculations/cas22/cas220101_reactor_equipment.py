import matplotlib
from io import BytesIO
from typing import Dict
from matplotlib import pyplot as plt
from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.data import CAS220101
from pyfecons.enums import ReactorType, BlanketFirstWall, BlanketType
from pyfecons.inputs import RadialBuild, Blanket
from pyfecons.materials import Materials, Material
from pyfecons.units import M_USD

matplotlib.use('Agg')


def compute_inner_radii(reactor_type: ReactorType, IN: RadialBuild, OUT: CAS220101):
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
        OUT.gap2_ir = OUT.lt_shield_ir + IN.lt_shield_t # Adjusted gap2 inner radius directly after lt_shield

    OUT.bioshield_ir = OUT.gap2_ir + IN.gap2_t  # Adjusted bioshield inner radius


def compute_outer_radii(reactor_type: ReactorType, IN: RadialBuild, OUT: CAS220101):
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
    OUT.lt_shield_or = OUT.lt_shield_ir + IN.lt_shield_t  # Adjusted lt_shield outer radius

    if reactor_type == ReactorType.MFE:
        OUT.coil_or = OUT.coil_ir + IN.coil_t  # Updated coil_or calculation

    OUT.gap2_or = OUT.gap2_ir + IN.gap2_t  # Adjusted gap2 outer radius directly after lt_shield
    OUT.bioshield_or = OUT.bioshield_ir + IN.bioshield_t  # Adjusted bioshield outer radius


def compute_first_wall_costs(blanket: Blanket, materials: Materials, OUT: CAS220101) -> M_USD:
    # First wall
    if blanket.first_wall == BlanketFirstWall.TUNGSTEN:
        return compute_material_cost(OUT.firstwall_vol, materials.W)
    elif blanket.first_wall == BlanketFirstWall.LIQUID_LITHIUM:
        return compute_material_cost(OUT.firstwall_vol, materials.Li)
    elif blanket.first_wall == BlanketFirstWall.BERYLLIUM:
        return compute_material_cost(OUT.firstwall_vol, materials.Be)
    elif blanket.first_wall == BlanketFirstWall.FLIBE:
        return compute_material_cost(OUT.firstwall_vol, materials.FliBe)
    raise f'Unknown first wall type {blanket.first_wall}'


def compute_blanket_costs(blanket: Blanket, materials: Materials, OUT: CAS220101) -> M_USD:
    # Blanket
    if blanket.blanket_type == BlanketType.FLOWING_LIQUID_FIRST_WALL:
        return compute_material_cost(OUT.blanket1_vol, materials.Li)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER:
        return compute_material_cost(OUT.blanket1_vol, materials.Li)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI4SIO4:
        return compute_material_cost(OUT.blanket1_vol, materials.Li4SiO4)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3:
        return compute_material_cost(OUT.blanket1_vol, materials.Li2TiO3)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_NO_BREEDER_ANEUTRONIC_FUEL:
        return M_USD(0)
    raise f'Unknown blanket type {blanket.blanket_type}'


def compute_material_cost(volume: float, material: Material) -> M_USD:
    return to_m_usd(volume * material.rho * material.c_raw * material.m)


def plot_radial_build(reactor_type: ReactorType, radial_build: RadialBuild) -> bytes:
    """
    PLOTTING RADIAL BUILD
    """
    IN = radial_build

    # The names of the sections
    # Updated order of the sections
    sections = ['Plasma', 'Vacuum', 'First Wall', 'Blanket', 'Reflector',
                'HT Shield', 'Structure', 'Gap', 'Vessel', 'LT Shield',
                *(['Coil'] if reactor_type == ReactorType.MFE else []),  # include only for MFE
                'Gap', 'Bioshield']

    # The thickness of each section (for stacked bar plot)
    thickness = [IN.plasma_t, IN.vacuum_t, IN.firstwall_t, IN.blanket1_t, IN.reflector_t,
                 IN.ht_shield_t, IN.structure_t, IN.gap1_t, IN.vessel_t, IN.lt_shield_t,
                 *([IN.coil_t] if reactor_type == ReactorType.MFE else []),  # include only for MFE
                 IN.gap2_t, IN.bioshield_t]

    # Updated colors for each section
    colors = ['purple', 'black', 'lightblue', 'darkblue', 'blue',
              'cornflowerblue', 'coral', 'lightgray', 'orange', 'slateblue',
              *(['green'] if reactor_type == ReactorType.MFE else []),  # include only for MFE
              'lightgray', 'darkorange']

    # Plotting the stacked bar graph
    fig, ax = plt.subplots(figsize=(18, 3.5))  # Adjust the figsize to get the desired aspect ratio

    # Adding each section to the bar plot
    left = 0  # Initialize left at 0
    for i, (section, thk) in enumerate(zip(sections, thickness)):
        ax.barh('Thickness', thk, left=left, color=colors[i], edgecolor='white', label=section)
        left += thk  # Increment left by the thickness of the current section

    # Setting labels and title
    ax.set_xlabel('Radius (m)')

    # Creating the legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # Show grid for the x-axis
    ax.xaxis.grid(True)

    # Show the plot
    plt.tight_layout()

    # save figure
    figure_data = BytesIO()
    fig.savefig(figure_data, format='pdf', bbox_inches='tight')
    figure_data.seek(0)
    plt.close(fig)
    return figure_data.read()


def compute_220101_replacements(reactor_type: ReactorType, blanket: Blanket,
                                IN: RadialBuild, OUT: CAS220101) -> Dict[str, str]:
    return {
        'C22010100': str(OUT.C220101),
        'C22010101': str(OUT.C22010101),
        'C22010102': str(OUT.C22010102),

        'primaryC': blanket.primary_coolant.display_name,
        'secondaryC': blanket.secondary_coolant.display_name,
        'neutronM': blanket.neutron_multiplier.display_name,
        'structure1': blanket.structure.display_name,
        'firstW': blanket.first_wall.display_name,

        'TH01': round(IN.plasma_t, 1),
        'TH02': round(IN.vacuum_t, 1),
        'TH03': round(IN.firstwall_t, 1),
        'TH04': round(IN.blanket1_t, 1),
        'TH05': round(IN.structure_t, 1),
        'TH06': round(IN.reflector_t, 1),
        'TH07': round(IN.gap1_t, 1),
        'TH08': round(IN.vessel_t, 1),
        'TH09': round(IN.ht_shield_t, 1),
        'TH10': round(IN.lt_shield_t, 1),
        **({'TH11': round(IN.coil_t, 1)} if reactor_type == ReactorType.MFE else {}),
        'TH12': round(IN.axis_t, 1),
        'TH13': round(IN.gap2_t, 1),
        'TH14': round(IN.bioshield_t, 1),

        'RAD1I': round(OUT.plasma_ir, 1),
        'RAD2I': round(OUT.vacuum_ir, 1),
        'RAD3I': round(OUT.firstwall_ir, 1),
        'RAD4I': round(OUT.blanket1_ir, 1),
        'RAD5I': round(OUT.structure_ir, 1),
        'RAD6I': round(OUT.reflector_ir, 1),
        'RAD7I': round(OUT.gap1_ir, 1),
        'RAD8I': round(OUT.vessel_ir, 1),
        'RAD9I': round(OUT.ht_shield_ir, 1),
        'RAD10I': round(OUT.lt_shield_ir, 1),
        **({'RAD11I': round(OUT.coil_ir, 1)} if reactor_type == ReactorType.MFE else {}),
        'RAD12I': round(OUT.axis_ir, 1),
        'RAD13I': round(OUT.gap2_ir, 1),
        'RAD14I': round(OUT.bioshield_ir, 1),

        'RAD1O': round(OUT.plasma_or, 1),
        'RAD2O': round(OUT.vacuum_or, 1),
        'RAD3O': round(OUT.firstwall_or, 1),
        'RAD4O': round(OUT.blanket1_or, 1),
        'RAD5O': round(OUT.structure_or, 1),
        'RAD6O': round(OUT.reflector_or, 1),
        'RAD7O': round(OUT.gap1_or, 1),
        'RAD8O': round(OUT.vessel_or, 1),
        'RAD9O': round(OUT.ht_shield_or, 1),
        'RAD10O': round(OUT.lt_shield_or, 1),
        **({'RAD11O': round(OUT.coil_or, 1)} if reactor_type == ReactorType.MFE else {}),
        'RAD12O': round(OUT.axis_or, 1),
        'RAD13O': round(OUT.gap2_or, 1),
        'RAD14O': round(OUT.bioshield_or, 1),

        'VOL01': round(OUT.plasma_vol, 1),
        'VOL02': round(OUT.vacuum_vol, 1),
        'VOL03': round(OUT.firstwall_vol, 1),
        'VOL04': round(OUT.blanket1_vol, 1),
        'VOL05': round(OUT.structure_vol, 1),
        'VOL06': round(OUT.reflector_vol, 1),
        'VOL07': round(OUT.gap1_vol, 1),
        'VOL08': round(OUT.vessel_vol, 1),
        'VOL09': round(OUT.ht_shield_vol, 1),
        'VOL10': round(OUT.lt_shield_vol, 1),
        **({'VOL11': round(OUT.coil_vol, 1)} if reactor_type == ReactorType.MFE else {}),
        'VOL12': round(OUT.axis_vol, 1),
        'VOL13': round(OUT.gap2_vol, 1),
        'VOL14': round(OUT.bioshield_vol, 1),
    }
