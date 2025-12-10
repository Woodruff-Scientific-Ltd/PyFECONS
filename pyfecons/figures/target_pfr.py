from io import BytesIO

import matplotlib
from matplotlib import pyplot as plt

from pyfecons.costing.calculations.interpolation import interpolate_plot
from pyfecons.costing.ife.pfr_costs import pertarget_pfr_coords, yearlytcost_pfr_coords

matplotlib.use("Agg")


class TargetPfrFigure:
    """Class for generating target pfr plots."""

    @staticmethod
    def create() -> bytes:
        coordinates1 = yearlytcost_pfr_coords
        coordinates2 = pertarget_pfr_coords

        # Creating a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))

        # Interpolating and plotting for the first set of coordinates
        interpolate_plot(
            ax1, coordinates1, "Yearly Total Cost vs Frequency", "Yearly cost (M$)"
        )

        # Interpolating and plotting for the second set of coordinates
        interpolate_plot(
            ax2, coordinates2, "Per Target Cost vs Frequency", "Cost per target ($)"
        )

        # save figure
        figure_data = BytesIO()
        fig.savefig(figure_data, format="pdf", bbox_inches="tight")
        figure_data.seek(0)
        plt.close(fig)
        return figure_data.read()
