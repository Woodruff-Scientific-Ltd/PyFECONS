from io import BytesIO

import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from pyfecons.inputs.power_supplies import PowerSupplies
from pyfecons.units import HZ

matplotlib.use("Agg")


class CapDerateFigure:
    """Class for generating cap derate plots."""

    @staticmethod
    def create(power: PowerSupplies, implosion_frequency: HZ) -> bytes:
        # Arrays for storing calculated values
        cap_v0 = np.zeros(100)
        cap_l2 = np.zeros(100)
        cap_cost_fac = np.zeros(100)

        cap_x = (power.cap_temp - power.cap_temp_ambient - power.cap_temp_delta) / 10

        # Loop for calculations
        for i in range(100):
            cap_v0[i] = (
                power.cap_voltage / 100 * (i + 1)
            )  # applied voltage in application
            cap_l2[i] = power.cap_l1 * (power.cap_voltage / cap_v0[i]) ** 7 * 2**cap_x
            cap_cost_fac[i] = 1 / (cap_v0[i] / power.cap_voltage) ** 2

        # TODO this is not used
        # Convert applied voltage from V to kV for plotting
        capv0_kV = cap_v0 / 1000  # Convert to kV

        # Re-plotting the third chart according to new specifications: not using standard form for y-axis and plotting in blue
        plt.figure(figsize=[15, 5])

        # Lifetime extension factor plot (unchanged)
        plt.subplot(1, 3, 1)
        plt.semilogy(cap_v0 / power.cap_voltage, cap_l2 / power.cap_l1, "b")
        plt.title("Lifetime Extension Factor")
        plt.xlabel("Ratio of applied to rated voltage")
        plt.ylabel("Lifetime extension factor, L2/L1")
        plt.axis([0, 1, 1, 100000])

        # Lifetime of bank in years plot (unchanged)
        plt.subplot(1, 3, 2)
        plt.semilogy(
            cap_v0 / power.cap_voltage,
            cap_l2 / (implosion_frequency * 86000 * 365),
            "b",
        )  # Assuming 86000 cycles per year
        plt.title("Lifetime of Bank in Years")
        plt.xlabel("Ratio of applied to rated voltage")
        plt.ylabel(f"Lifetime of bank in years, at {implosion_frequency} Hz")
        plt.axis([0, 1, 0.001, 100])

        # Bank cost factor plot with specified changes
        plt.subplot(1, 3, 3)
        plt.plot(cap_v0 / power.cap_voltage, cap_cost_fac, "b")  # Changed to blue color
        plt.title("Bank Cost Factor")
        plt.xlabel("Ratio of applied to rated voltage")
        plt.ylabel("Bank cost factor")
        plt.yscale("linear")  # Changed to linear scale
        plt.axis([0, 1, 1, 100])

        # Show updated plots
        plt.tight_layout()

        # Plotting the stacked bar graph
        # Adjust the figsize to get the desired aspect ratio
        fig, ax = plt.subplots(figsize=(18, 3.5))

        # save figure
        figure_data = BytesIO()
        fig.savefig(figure_data, format="pdf", bbox_inches="tight")
        figure_data.seek(0)
        plt.close(fig)
        return figure_data.read()
