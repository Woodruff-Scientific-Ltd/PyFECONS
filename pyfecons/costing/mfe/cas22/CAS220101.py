import numpy as np
import matplotlib
from io import BytesIO
from matplotlib import pyplot as plt
from pyfecons.costing.calculations.conversions import to_m_usd
from pyfecons.data import Data, TemplateProvider
from pyfecons.enums import BlanketFirstWall, BlanketType
from pyfecons.inputs import Inputs, RadialBuild
from pyfecons.units import Meters3, Meters, M_USD

matplotlib.use('Agg')


def cas_220101_reactor_equipment(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.1: Reactor Equipment
    IN = inputs.radial_build
    OUT = data.cas220101
    blanket = inputs.blanket
    materials = inputs.materials

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
    OUT.lt_shield_ir = OUT.vessel_ir + IN.vessel_t  # Moved lt_shield here
    OUT.coil_ir = OUT.lt_shield_ir + IN.lt_shield_t  # Updated coil_ir calculation
    OUT.gap2_ir = OUT.coil_ir + IN.coil_t
    OUT.bioshield_ir = OUT.gap2_ir + IN.gap2_t  # Updated bioshield inner radius

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
    OUT.lt_shield_or = OUT.lt_shield_ir + IN.lt_shield_t  # Moved lt_shield here
    OUT.coil_or = OUT.coil_ir + IN.coil_t  # Updated coil_or calculation
    OUT.gap2_or = OUT.gap2_ir + IN.gap2_t
    OUT.bioshield_or = OUT.bioshield_ir + IN.bioshield_t  # Updated bioshield outer radius

    def calc_volume_torus(inner, outer):
        return Meters3(2 * np.pi * IN.axis_t * np.pi * (inner + outer) ** 2)

    OUT.axis_vol = 0.0
    OUT.plasma_vol = Meters3(IN.elon * calc_volume_torus(OUT.plasma_ir, IN.plasma_t) - OUT.axis_vol)
    OUT.vacuum_vol = Meters3(IN.elon * calc_volume_torus(OUT.vacuum_ir, IN.vacuum_t)
                             - sum([OUT.plasma_vol, OUT.axis_vol]))
    OUT.firstwall_vol = Meters3(IN.elon * calc_volume_torus(OUT.firstwall_ir, IN.firstwall_t)
                                - sum([OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.blanket1_vol = Meters3(IN.elon * calc_volume_torus(OUT.blanket1_ir, IN.blanket1_t)
                               - sum([OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.reflector_vol = Meters3(IN.elon * calc_volume_torus(OUT.reflector_ir, IN.reflector_t)
                                - sum([OUT.blanket1_vol, OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol,
                                       OUT.axis_vol]))
    OUT.ht_shield_vol = Meters3(IN.elon * calc_volume_torus(OUT.ht_shield_ir, IN.ht_shield_t)
                                - sum([OUT.reflector_vol, OUT.blanket1_vol, OUT.firstwall_vol,
                                       OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.structure_vol = Meters3(IN.elon * calc_volume_torus(OUT.structure_ir, IN.structure_t)
                                - sum([OUT.ht_shield_vol, OUT.reflector_vol, OUT.blanket1_vol, OUT.firstwall_vol,
                                       OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.gap1_vol = Meters3(IN.elon * calc_volume_torus(OUT.gap1_ir, IN.gap1_t)
                           - sum([OUT.structure_vol, OUT.ht_shield_vol, OUT.reflector_vol, OUT.blanket1_vol,
                                  OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.vessel_vol = Meters3(IN.elon * calc_volume_torus(OUT.vessel_ir, IN.vessel_t)
                             - sum([OUT.gap1_vol, OUT.structure_vol, OUT.ht_shield_vol, OUT.reflector_vol,
                                    OUT.blanket1_vol, OUT.firstwall_vol, OUT.vacuum_vol, OUT.plasma_vol, OUT.axis_vol]))
    OUT.lt_shield_vol = Meters3(IN.elon * calc_volume_torus(OUT.lt_shield_ir, IN.lt_shield_t)
                                - sum([OUT.vessel_vol, OUT.gap1_vol, OUT.structure_vol, OUT.ht_shield_vol,
                                       OUT.reflector_vol, OUT.blanket1_vol, OUT.firstwall_vol, OUT.vacuum_vol,
                                       OUT.plasma_vol, OUT.axis_vol]))
    OUT.coil_vol = Meters3(calc_volume_torus(OUT.coil_ir, IN.coil_t) * 0.5)

    def calc_volume_ring(height: Meters, outer: Meters, inner: Meters) -> Meters3:
        return Meters3(height * np.pi * (outer ** 2 - inner ** 2))

    # must be cylindrical in all cases
    OUT.gap2_vol = calc_volume_ring(IN.axis_t, IN.gap2_t + OUT.gap2_ir, OUT.gap2_ir)
    # Updated bioshield volume
    OUT.bioshield_vol = calc_volume_ring(IN.axis_t, IN.bioshield_t + OUT.bioshield_ir, OUT.bioshield_ir)

    # First wall
    if blanket.first_wall == BlanketFirstWall.TUNGSTEN:
        OUT.C22010101 = to_m_usd(OUT.firstwall_vol * materials.W.rho * materials.W.c_raw * materials.W.m)
    elif blanket.first_wall == BlanketFirstWall.LIQUID_LITHIUM:
        OUT.C22010101 = to_m_usd(OUT.firstwall_vol * materials.Li.rho * materials.Li.c_raw * materials.Li.m)
    elif blanket.first_wall == BlanketFirstWall.BERYLLIUM:
        OUT.C22010101 = to_m_usd(OUT.firstwall_vol * materials.Be.rho * materials.Be.c_raw * materials.Be.m)
    elif blanket.first_wall == BlanketFirstWall.FLIBE:
        OUT.C22010101 = to_m_usd(OUT.firstwall_vol * materials.FliBe.rho * materials.FliBe.c_raw * materials.FliBe.m)

    # Blanket
    if blanket.blanket_type == BlanketType.FLOWING_LIQUID_FIRST_WALL:
        OUT.C22010102 = to_m_usd(OUT.blanket1_vol * materials.Li.rho * materials.Li.c_raw * materials.Li.m)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_WITH_A_LIQUID_BREEDER:
        OUT.C22010102 = to_m_usd(OUT.blanket1_vol * materials.Li.rho * materials.Li.c_raw * materials.Li.m)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI4SIO4:
        OUT.C22010102 = to_m_usd(OUT.blanket1_vol * materials.Li4SiO4.rho * materials.Li4SiO4.c_raw * materials.Li4SiO4.m)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI2TIO3:
        OUT.C22010102 = to_m_usd(OUT.blanket1_vol * materials.Li2TiO3.rho * materials.Li2TiO3.c_raw * materials.Li2TiO3.m)
    elif blanket.blanket_type == BlanketType.SOLID_FIRST_WALL_NO_BREEDER_ANEUTRONIC_FUEL:
        OUT.C22010102 = M_USD(0)

    # Total cost of blanket and first wall
    OUT.C220101 = M_USD(OUT.C22010101 + OUT.C22010102)

    OUT.figures['Figures/radial_build.pdf'] = plot_radial_build(IN)

    OUT.template_file = 'CAS220101_MFE_DT.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C22010100': str(data.cas220101.C220101),
        'C22010101': str(data.cas220101.C22010101),
        'C22010102': str(data.cas220101.C22010102),

        'primaryC': inputs.blanket.primary_coolant.display_name,
        'secondaryC': inputs.blanket.secondary_coolant.display_name,
        'neutronM': inputs.blanket.neutron_multiplier.display_name,
        'structure1': inputs.blanket.structure.display_name,
        'firstW': inputs.blanket.first_wall.display_name,

        'TH01': round(inputs.radial_build.plasma_t, 1),
        'TH02': round(inputs.radial_build.vacuum_t, 1),
        'TH03': round(inputs.radial_build.firstwall_t, 1),
        'TH04': round(inputs.radial_build.blanket1_t, 1),
        'TH05': round(inputs.radial_build.structure_t, 1),
        'TH06': round(inputs.radial_build.reflector_t, 1),
        'TH07': round(inputs.radial_build.gap1_t, 1),
        'TH08': round(inputs.radial_build.vessel_t, 1),
        'TH09': round(inputs.radial_build.ht_shield_t, 1),
        'TH10': round(inputs.radial_build.lt_shield_t, 1),
        'TH11': round(inputs.radial_build.coil_t, 1),
        'TH12': round(inputs.radial_build.axis_t, 1),
        'TH13': round(inputs.radial_build.gap2_t, 1),
        'TH14': round(inputs.radial_build.bioshield_t, 1),

        'RAD1I': round(data.cas220101.plasma_ir, 1),
        'RAD2I': round(data.cas220101.vacuum_ir, 1),
        'RAD3I': round(data.cas220101.firstwall_ir, 1),
        'RAD4I': round(data.cas220101.blanket1_ir, 1),
        'RAD5I': round(data.cas220101.structure_ir, 1),
        'RAD6I': round(data.cas220101.reflector_ir, 1),
        'RAD7I': round(data.cas220101.gap1_ir, 1),
        'RAD8I': round(data.cas220101.vessel_ir, 1),
        'RAD9I': round(data.cas220101.ht_shield_ir, 1),
        'RAD10I': round(data.cas220101.lt_shield_ir, 1),
        'RAD11I': round(data.cas220101.coil_ir, 1),
        'RAD12I': round(data.cas220101.axis_ir, 1),
        'RAD13I': round(data.cas220101.gap2_ir, 1),
        'RAD14I': round(data.cas220101.bioshield_ir, 1),

        'RAD1O': round(data.cas220101.plasma_or, 1),
        'RAD2O': round(data.cas220101.vacuum_or, 1),
        'RAD3O': round(data.cas220101.firstwall_or, 1),
        'RAD4O': round(data.cas220101.blanket1_or, 1),
        'RAD5O': round(data.cas220101.structure_or, 1),
        'RAD6O': round(data.cas220101.reflector_or, 1),
        'RAD7O': round(data.cas220101.gap1_or, 1),
        'RAD8O': round(data.cas220101.vessel_or, 1),
        'RAD9O': round(data.cas220101.ht_shield_or, 1),
        'RAD10O': round(data.cas220101.lt_shield_or, 1),
        'RAD11O': round(data.cas220101.coil_or, 1),
        'RAD12O': round(data.cas220101.axis_or, 1),
        'RAD13O': round(data.cas220101.gap2_or, 1),
        'RAD14O': round(data.cas220101.bioshield_or, 1),

        'VOL01': round(data.cas220101.plasma_vol, 1),
        'VOL02': round(data.cas220101.vacuum_vol, 1),
        'VOL03': round(data.cas220101.firstwall_vol, 1),
        'VOL04': round(data.cas220101.blanket1_vol, 1),
        'VOL05': round(data.cas220101.structure_vol, 1),
        'VOL06': round(data.cas220101.reflector_vol, 1),
        'VOL07': round(data.cas220101.gap1_vol, 1),
        'VOL08': round(data.cas220101.vessel_vol, 1),
        'VOL09': round(data.cas220101.ht_shield_vol, 1),
        'VOL10': round(data.cas220101.lt_shield_vol, 1),
        'VOL11': round(data.cas220101.coil_vol, 1),
        'VOL12': round(data.cas220101.axis_vol, 1),
        'VOL13': round(data.cas220101.gap2_vol, 1),
        'VOL14': round(data.cas220101.bioshield_vol, 1),
    }
    return OUT


def plot_radial_build(radial_build: RadialBuild) -> bytes:
    """
    PLOTTING RADIAL BUILD
    """
    IN = radial_build

    # The names of the sections
    # Updated order of the sections
    sections = ['Plasma', 'Vacuum', 'First Wall', 'Blanket', 'Reflector', 'HT Shield', 'Structure', 'Gap', 'Vessel',
                'LT Shield', 'Coil', 'Gap', 'Bioshield']

    # The thickness of each section (for stacked bar plot)
    thickness = [IN.plasma_t, IN.vacuum_t, IN.firstwall_t, IN.blanket1_t, IN.reflector_t, IN.ht_shield_t,
                 IN.structure_t, IN.gap1_t, IN.vessel_t, IN.lt_shield_t, IN.coil_t, IN.gap2_t, IN.bioshield_t]

    # Updated colors for each section
    colors = ['purple', 'black', 'lightblue', 'darkblue', 'blue', 'cornflowerblue', 'coral', 'lightgray', 'orange',
              'slateblue', 'green', 'lightgray', 'darkorange']

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

    # save figure
    figure_data = BytesIO()
    fig.savefig(figure_data, format='pdf', bbox_inches='tight')
    figure_data.seek(0)
    plt.close(fig)
    return figure_data.read()
