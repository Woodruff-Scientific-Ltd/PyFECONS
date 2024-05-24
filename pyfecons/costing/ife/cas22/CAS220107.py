import numpy as np
import matplotlib

from io import BytesIO
from matplotlib import pyplot as plt
from pyfecons.data import Data, TemplateProvider
from pyfecons.inputs import Inputs, PowerSupplies
from pyfecons.units import M_USD, HZ

matplotlib.use('Agg')


def cas_220107_power_supplies(inputs: Inputs, data: Data) -> TemplateProvider:
    # Cost Category 22.1.7 Power supplies
    IN = inputs.power_supplies
    OUT = data.cas220107
    basic = inputs.basic

    # Power supplies for confinement
    OUT.C22010701 = M_USD(IN.p_compress * basic.implosion_frequency * IN.cost_per_watt)

    # Scaled relative to ITER for a 500MW fusion power system
    # assuming 1kIUA equals $2 M #cost in kIUA
    OUT.C22010702 = M_USD(269.6 * basic.p_nrl/500 * IN.learning_credit * 2)
    OUT.C220107 = M_USD(OUT.C22010701 + OUT.C22010702)

    # TODO - is this ever a value?
    # scaled relative to the Woodruff Scientific PF bank designed for FLARE: 200kV, 400kA, 0.5MJ
    # C22010702 = 30
    # C220107 = 30

    OUT.figures['Figures/cap_derate.pdf'] = generate_cap_derate_figure(IN, basic.implosion_frequency)

    OUT.template_file = 'CAS220107_IFE.tex'
    OUT.tex_path = 'Modified/' + OUT.template_file
    OUT.replacements = {
        'C22010700': round(OUT.C220107),
        'C22010701': round(OUT.C22010701),  # TODO not in template
        'C22010702': round(OUT.C22010702),  # TODO not in template
        'PNRL': round(basic.p_nrl),
    }
    return OUT


# TODO figure is not rendering anything and it's not used in the template
def generate_cap_derate_figure(IN: PowerSupplies, implosion_frequency: HZ) -> bytes:
    # Arrays for storing calculated values
    cap_v0 = np.zeros(100)
    cap_l2 = np.zeros(100)
    cap_cost_fac = np.zeros(100)

    cap_x = (IN.cap_temp - IN.cap_temp_ambient - IN.cap_temp_delta) / 10

    # Loop for calculations
    for i in range(100):
        cap_v0[i] = IN.cap_voltage / 100 * (i + 1)  # applied voltage in application
        cap_l2[i] = IN.cap_l1 * (IN.cap_voltage / cap_v0[i]) ** 7 * 2 ** cap_x
        cap_cost_fac[i] = 1 / (cap_v0[i] / IN.cap_voltage) ** 2

    # TODO this is not used
    # Convert applied voltage from V to kV for plotting
    capv0_kV = cap_v0 / 1000  # Convert to kV

    # Re-plotting the third chart according to new specifications: not using standard form for y-axis and plotting in blue
    plt.figure(figsize=[15, 5])

    # Lifetime extension factor plot (unchanged)
    plt.subplot(1, 3, 1)
    plt.semilogy(cap_v0 / IN.cap_voltage, cap_l2 / IN.cap_l1, 'b')
    plt.title('Lifetime Extension Factor')
    plt.xlabel('Ratio of applied to rated voltage')
    plt.ylabel('Lifetime extension factor, L2/L1')
    plt.axis([0, 1, 1, 100000])

    # Lifetime of bank in years plot (unchanged)
    plt.subplot(1, 3, 2)
    plt.semilogy(cap_v0 / IN.cap_voltage, cap_l2 / (implosion_frequency * 86000 * 365), 'b')  # Assuming 86000 cycles per year
    plt.title('Lifetime of Bank in Years')
    plt.xlabel('Ratio of applied to rated voltage')
    plt.ylabel(f'Lifetime of bank in years, at {implosion_frequency} Hz')
    plt.axis([0, 1, 0.001, 100])

    # Bank cost factor plot with specified changes
    plt.subplot(1, 3, 3)
    plt.plot(cap_v0 / IN.cap_voltage, cap_cost_fac, 'b')  # Changed to blue color
    plt.title('Bank Cost Factor')
    plt.xlabel('Ratio of applied to rated voltage')
    plt.ylabel('Bank cost factor')
    plt.yscale('linear')  # Changed to linear scale
    plt.axis([0, 1, 1, 100])

    # Show updated plots
    plt.tight_layout()
    plt.show()

    # Plotting the stacked bar graph
    # Adjust the figsize to get the desired aspect ratio
    fig, ax = plt.subplots(figsize=(18, 3.5))

    # save figure
    figure_data = BytesIO()
    fig.savefig(figure_data, format='pdf', bbox_inches='tight')
    figure_data.seek(0)
    plt.close(fig)
    return figure_data.read()
