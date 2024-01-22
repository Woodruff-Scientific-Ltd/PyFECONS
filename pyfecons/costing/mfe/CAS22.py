from pyfecons.inputs import Inputs
from pyfecons.data import Data
import math
import matplotlib.pyplot as plt

def GenerateData(inputs: Inputs, data:Data, figures:dict):

    basic = inputs.basic
    IN = inputs.radial_build
    OUT = data.cas22
    
    #Cost Category 22.1.1: Reactor Equipment
    # Inner radii
    OUT.axis_ir = IN.axis_t
    OUT.plasma_ir = IN.plasma_t
    OUT.vacuum_ir = IN.vacuum_t + IN.plasma_t
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

    def calc_volume(inner, outer):
        return IN.chamber_length * math.pi * (outer**2 - inner**2)

    # Volumes for cylinder
    OUT.axis_vol = calc_volume(OUT.axis_ir, OUT.axis_or)
    OUT.plasma_vol = calc_volume(OUT.plasma_ir, OUT.plasma_or)
    OUT.vacuum_vol = calc_volume(OUT.vacuum_ir, OUT.vacuum_or)
    OUT.firstwall_vol = calc_volume(OUT.firstwall_ir, OUT.firstwall_or)
    OUT.blanket1_vol = calc_volume(OUT.blanket1_ir, OUT.blanket1_or)
    OUT.reflector_vol = calc_volume(OUT.reflector_ir, OUT.reflector_or)
    OUT.ht_shield_vol = calc_volume(OUT.ht_shield_ir, OUT.ht_shield_or)
    OUT.structure_vol = calc_volume(OUT.structure_ir, OUT.structure_or)
    OUT.gap1_vol = calc_volume(OUT.gap1_ir, OUT.gap1_or)
    OUT.vessel_vol = calc_volume(OUT.vessel_ir, OUT.vessel_or)
    OUT.lt_shield_vol = calc_volume(OUT.lt_shield_ir, OUT.lt_shield_or)  # Moved lt_shield volume here
    OUT.coil_vol = calc_volume(OUT.coil_ir, OUT.coil_or)*(9*0.779)/40  # Updated coil volume calculation
    OUT.gap2_vol = calc_volume(OUT.gap2_ir, OUT.gap2_or)
    OUT.bioshield_vol = calc_volume(OUT.bioshield_ir, OUT.bioshield_or)  # Updated bioshield volume


    #Cost calc 1

    # Define the values
    f_W = 1
    C_OFW = 0
    M_OFW = 0
    # Blanket is rotating vortex of PbLi
    FPCPPFbLi = 0.9
    f_FS = 0.1
    # Cost of blanket
    C_OBI_PbLi = OUT.blanket1_vol * (inputs.materials.PbLi.rho * inputs.materials.PbLi.c * FPCPPFbLi)
    C_OBI_FS = OUT.blanket1_vol * (inputs.materials.FS.rho * inputs.materials.FS.c_raw * f_FS)
    # Total heat capacity of OBI
    C_OBI = C_OBI_FS + C_OBI_PbLi
    # Calculate C_22_1_1
    C220101 = basic.am * basic.n_mod * (C_OFW + C_OBI) / 1e6  # First Wall/Blanket/reflector


    

    """
    PLOTTING RADIAL BUILD
    """

    ## The names of the sections
    # Updated order of the sections
    sections = ['Plasma', 'Vacuum', 'First Wall', 'Blanket', 'Reflector', 'HT Shield', 'Structure', 'Gap', 'Vessel', 'LT Shield', 'Coil', 'Gap', 'Bioshield']

    # The thickness of each section (for stacked bar plot)
    thickness = [IN.plasma_t, IN.vacuum_t, IN.firstwall_t, IN.blanket1_t, IN.reflector_t, IN.ht_shield_t, IN.structure_t, IN.gap1_t, IN.vessel_t, IN.lt_shield_t, IN.coil_t, IN.gap2_t, IN.bioshield_t]

    # Updated colors for each section
    colors = ['purple', 'black', 'lightblue', 'darkblue', 'blue', 'cornflowerblue', 'coral', 'lightgray', 'orange', 'slateblue', 'green', 'lightgray', 'darkorange']

    # Plotting the stacked bar graph
    fig, ax = plt.subplots(figsize=(18, 3.5)) # Adjust the figsize to get the desired aspect ratio

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
    plt.show()

    figures["radial_build.pdf"] = fig

    # Export as pdf
    #fig.savefig(os.path.join(figures_directory, 'radial_build.pdf'), bbox_inches='tight')



    # copy_file('CAS220101_MFE_DT.tex')
    # overwrite_variable('CAS220101_MFE_DT.tex', 'C220101', round(C220101))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD12I', round(coil_ir))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD13I', round(bioshield_ir))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD10I', round(gap2_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD11I', round(lt_shield_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD1I', round(plasma_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD2I', round(vacuum_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD3I', round(firstwall_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD4I', round(blanket1_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD5I', round(structure_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD6I', round(reflector_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD7I', round(gap1_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD8I', round(vessel_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD9I', round(ht_shield_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD12O', round(coil_or))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD13O', round(bioshield_or))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD10O', round(gap2_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD11O', round(lt_shield_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD1O', round(plasma_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD2O', round(vacuum_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD3O', round(firstwall_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD4O', round(blanket1_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD5O', round(structure_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD6O', round(reflector_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD7O', round(gap1_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD8O', round(vessel_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'RAD9O', round(ht_shield_or,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH10', round(gap2_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH11', round(lt_shield_t))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH12', round(coil_t))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH13', round(bioshield_t))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH1', round(plasma_t,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH2', round(vacuum_t,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH3', round(firstwall_t,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH4', round(blanket1_t,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH5', round(structure_t,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH6', round(reflector_t,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH7', round(gap1_t,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH8', round(vessel_t,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'TH9', round(ht_shield_t,1))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL10', round(gap2_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL11', round(lt_shield_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL12', round(coil_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL13', round(bioshield_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL1', round(plasma_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL2', round(vacuum_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL3', round(firstwall_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL4', round(blanket1_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL5', round(structure_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL6', round(reflector_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL7', round(gap1_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL8', round(vessel_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'VOL9', round(ht_shield_vol))
    # overwrite_variable('CAS220101_MFE_DT.tex', 'primaryC', primaryC)
    # overwrite_variable('CAS220101_MFE_DT.tex', 'secondaryC', secondaryC)
    # overwrite_variable('CAS220101_MFE_DT.tex', 'neutronM', neutronM)
    # overwrite_variable('CAS220101_MFE_DT.tex', 'structure1', structure1)
    # overwrite_variable('CAS220101_MFE_DT.tex', 'firstW', firstW)