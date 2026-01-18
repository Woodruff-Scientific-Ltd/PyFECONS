from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt

from pyfecons.costing_data import CostingData

matplotlib.use("Agg")


class CostAccountingPieCharts:
    """Class for generating cost accounting pie charts."""

    @staticmethod
    def create(costing_data: CostingData) -> dict[str, bytes]:
        """
        Create three pie charts for cost accounting breakdown.

        Args:
            costing_data: The costing data containing all CAS categories

        Returns:
            A dictionary mapping figure names to PDF bytes
        """
        tcc = costing_data.cas90.C990000
        direct_costs = costing_data.cas20.C200000
        reactor_equip = costing_data.cas22.C220100

        figures = {}

        # Chart 1: % of TCC
        figures["tcc_pie_chart"] = CostAccountingPieCharts._create_tcc_chart(
            costing_data, tcc
        )

        # Chart 2: % of Direct Costs
        figures["direct_costs_pie_chart"] = (
            CostAccountingPieCharts._create_direct_costs_chart(
                costing_data, direct_costs
            )
        )

        # Chart 3: % of Reactor Plant Equipment
        figures["reactor_equip_pie_chart"] = (
            CostAccountingPieCharts._create_reactor_equip_chart(
                costing_data, reactor_equip
            )
        )

        return figures

    @staticmethod
    def _create_tcc_chart(costing_data: CostingData, tcc: float) -> bytes:
        """Create pie chart for % of TCC breakdown."""
        labels = [
            "Preconstruction",
            "Direct Costs",
            "Capitalized Indirect Service Costs",
            "Capitalized Owner's Cost",
            "Capitalized Supplementary Costs",
            "Capitalized Financial Costs",
        ]
        values = [
            costing_data.cas10.C100000,
            costing_data.cas20.C200000,
            costing_data.cas30.C300000,
            costing_data.cas40.C400000,
            costing_data.cas50.C500000,
            costing_data.cas60.C600000,
        ]
        colors = [
            "darkblue",
            "orange",
            "darkgreen",
            "lightblue",
            "purple",
            "lightgreen",
        ]

        return CostAccountingPieCharts._create_pie_chart(
            labels, values, tcc, "% of Total Capital Cost", colors
        )

    @staticmethod
    def _create_direct_costs_chart(
        costing_data: CostingData, direct_costs: float
    ) -> bytes:
        """Create pie chart for % of Direct Costs breakdown."""
        labels = [
            "Structures/Site",
            "Reactor Plant Equip.",
            "Turbine Plant Equip",
            "Electric Plant Equip",
            "Misc. Plant Equip",
            "Heat Rejection",
            "Special Materials",
            "Digital Twin",
            "Contingency",
        ]
        values = [
            costing_data.cas21.C210000,
            costing_data.cas22.C220000,
            costing_data.cas23.C230000,
            costing_data.cas24.C240000,
            costing_data.cas25.C250000,
            costing_data.cas26.C260000,
            costing_data.cas27.C270000,
            costing_data.cas28.C280000,
            costing_data.cas29.C290000 if costing_data.cas29.C290000 is not None else 0,
        ]
        colors = [
            "darkblue",  # Structures/Site
            "orange",  # Reactor Plant Equip.
            "darkgreen",  # Turbine Plant Equip
            "lightblue",  # Electric Plant Equip
            "purple",  # Misc. Plant Equip
            "lightgreen",  # Heat Rejection
            "darkgrey",  # Special Materials
            "brown",  # Digital Twin
            "green",  # Contingency
        ]

        return CostAccountingPieCharts._create_pie_chart(
            labels, values, direct_costs, "% of Direct Costs", colors
        )

    @staticmethod
    def _create_reactor_equip_chart(
        costing_data: CostingData, reactor_equip: float
    ) -> bytes:
        """Create pie chart for % of Reactor Plant Equipment breakdown."""
        labels = [
            "First Wall & Blanket",
            "High Temp. Shield",
            "Magnets",
            "Supplemental Heating",
            "Primary Structure",
            "Vacuum System",
            "Power Supplies",
            "Divertor",
            "Direct Energy Conversion",
            "Assembly and Installation",
        ]
        values = [
            costing_data.cas220101.C220101,
            costing_data.cas220102.C220102,
            costing_data.cas220103.C220103,
            costing_data.cas220104.C220104,
            costing_data.cas220105.C220105,
            costing_data.cas220106.C220106,
            costing_data.cas220107.C220107,
            costing_data.cas220108.C220108,
            costing_data.cas220109.C220109,
            costing_data.cas220111.C220111,
        ]
        # Colors matching the image descriptions
        # First Wall & Blanket: dark green, Primary Structure: dark teal
        colors = [
            "darkgreen",  # First Wall & Blanket
            "orange",  # High Temp. Shield
            "green",  # Magnets (medium green)
            "lightblue",  # Supplemental Heating
            "teal",  # Primary Structure (dark teal)
            "lightgreen",  # Vacuum System
            "darkblue",  # Power Supplies
            "darkred",  # Divertor
            "black",  # Direct Energy Conversion
            "purple",  # Assembly and Installation
        ]

        return CostAccountingPieCharts._create_pie_chart(
            labels, values, reactor_equip, "% of Reactor Plant Equipment", colors
        )

    @staticmethod
    def _create_pie_chart(
        labels: list[str],
        values: list[float],
        total: float,
        title: str,
        colors: list[str],
    ) -> bytes:
        """Create a pie chart with labels, percentages, and legend."""
        # Filter out zero values to avoid cluttering the chart
        filtered_data = [
            (label, v, c) for label, v, c in zip(labels, values, colors) if v > 0
        ]
        if not filtered_data:
            # If all values are zero, create empty chart
            filtered_data = [
                (label, v, c) for label, v, c in zip(labels, values, colors)
            ]

        # Sort by value in descending order (highest costs first)
        filtered_data = sorted(filtered_data, key=lambda x: x[1], reverse=True)

        filtered_labels, filtered_values, filtered_colors = zip(*filtered_data)

        # Calculate percentages
        percentages = [v / total * 100 if total > 0 else 0 for v in filtered_values]

        # Create the pie chart - slightly smaller to fit more on a page
        fig, ax = plt.subplots(figsize=(9, 7))

        # Create pie chart with autopct for percentage labels
        wedges, texts, autotexts = ax.pie(
            filtered_values,
            labels=None,  # We'll use legend instead
            autopct=lambda pct: f"{pct:.2f}%" if pct > 1 else "",
            colors=filtered_colors,
            startangle=90,
            textprops={"fontsize": 9},
        )

        # Create legend with labels, percentages, and cost values
        # Format values as billions (B) if >= 1000M, otherwise millions (M)
        # Show 2 decimal places but remove trailing zeros
        def format_cost(value: float) -> str:
            """Format cost value as $YY.YM or $YY.YYB depending on magnitude, removing trailing zeros."""
            if value >= 1000:
                # Format billions with 2 decimals, remove trailing zeros
                formatted = f"{value/1000:.2f}".rstrip("0").rstrip(".")
                return f"${formatted}B"
            else:
                # Format millions with 2 decimals, remove trailing zeros
                formatted = f"{value:.2f}".rstrip("0").rstrip(".")
                return f"${formatted}M"

        legend_labels = [
            f"{label}: {percent:.2f}% ({format_cost(value)})"
            for label, percent, value in zip(
                filtered_labels, percentages, filtered_values
            )
        ]
        ax.legend(
            wedges,
            legend_labels,
            title="",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=9,
        )

        plt.tight_layout()

        # Save figure as PNG with minimal padding to reduce space
        figure_data = BytesIO()
        fig.savefig(
            figure_data, format="png", bbox_inches="tight", pad_inches=0.05, dpi=150
        )
        figure_data.seek(0)
        plt.close(fig)
        return figure_data.read()
