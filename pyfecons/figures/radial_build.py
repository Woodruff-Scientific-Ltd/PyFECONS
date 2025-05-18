import matplotlib
import matplotlib.pyplot as plt

from io import BytesIO
from pyfecons.enums import ReactorType
from pyfecons.inputs.radial_build import RadialBuild

matplotlib.use("Agg")


class RadialBuildFigure:
    """Class for generating radial build plots."""

    @staticmethod
    def create(reactor_type: ReactorType, radial_build: RadialBuild) -> bytes:
        """
        Plot the radial build of the reactor.

        Args:
            reactor_type: The type of reactor (MFE or IFE)
            radial_build: The radial build data

        Returns:
            The plot as a PDF in bytes
        """
        IN = radial_build

        # The names of the sections
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
            *(
                ["Coil"] if reactor_type == ReactorType.MFE else []
            ),  # include only for MFE
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
            *(
                ["green"] if reactor_type == ReactorType.MFE else []
            ),  # include only for MFE
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
