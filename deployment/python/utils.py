import os

import pandas as pd
import psutil
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d
from scipy.stats import skewnorm
from plotnine import (
    ggplot,
    aes,
    geom_line,
    scale_color_manual,
    ggtitle,
    theme_minimal,
    scale_x_continuous,
)

# Path to the downloaded Natural Earth data
shapefile_path = "data/us_geo/us_counties.shp"


def energyTWhToCarbonOutputKG(fleet_energy, fleet_type, typeChars, percent_CCS):
    BTUFuel = np.array([typeChars.loc[t, "BTUFuel/kWhelec"] for t in fleet_type])
    kgCO2 = np.array([typeChars.loc[t, "kgCO2perMMBTU"] for t in fleet_type])
    carbon = fleet_energy * BTUFuel * kgCO2 * 10 ** (-6) * 10**9
    carbon *= 1 - percent_CCS
    return carbon


def capacityMWToEnergyTWh(fleet_capacity, fleet_type, typeChars):
    cap_factors = np.array([typeChars.loc[t, "CapFactor"] for t in fleet_type])
    return fleet_capacity * cap_factors * 8760 / (10**2 * 10**6)


def kgToGTons(kgs):
    return kgs * 10 ** (-12)


def mav(x, n=5):
    return uniform_filter1d(x, size=n)


def s_curve(T_ADOPT, k, t):
    return k / (1 + np.exp((np.log(1 / 19) - np.log(19)) / T_ADOPT * (t - T_ADOPT)))


# State abbreviations and names mapping
state_abbrev = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}


# Example of plotting S-curves
def plot_s_curves():
    x = np.arange(-25, 101)
    for T_ADOPT in [5, 10, 20, 30, 40, 50]:
        y = s_curve(T_ADOPT, 1, x)
        plt.plot(x, y, label=f"T_ADOPT={T_ADOPT}")

    plt.title("Sample S-curves")
    plt.ylabel("Percent Penetration")
    plt.ylim(0, 1)
    plt.xlabel("Time")
    plt.legend()
    plt.show()


def log_memory_usage(message):
    process = psutil.Process(os.getpid())
    print(f"Memory usage at {message}: {process.memory_info().rss / 1024 ** 2:.2f} MB")


def get_usa_maps():
    # Load map data for the USA
    usaMap = gpd.read_file(shapefile_path)
    usaMap["locCode"] = usaMap["STUSPS"].str.lower() + "," + usaMap["NAME"].str.lower()

    # Reproject to a suitable projected CRS (e.g., EPSG:3857)
    usaMap = usaMap.to_crs(epsg=3857)

    # Create a lookup table with unique location codes
    usaMap2 = usaMap.drop_duplicates(subset="locCode").set_index("locCode")
    usaMap2["long"] = usaMap2["geometry"].centroid.x
    usaMap2["lat"] = usaMap2["geometry"].centroid.y

    return usaMap, usaMap2


def rsnorm(size, mean, sd, xi):
    """
    Generate random numbers from a skew-normal distribution.

    :param size: Number of random numbers to generate.
    :param mean: Mean of the distribution.
    :param sd: Standard deviation of the distribution.
    :param xi: Skewness parameter.
    :return: Array of random numbers from the skew-normal distribution.
    """
    alpha = xi  # skewness parameter
    loc = mean  # location parameter
    scale = sd  # scale parameter

    return skewnorm.rvs(a=alpha, loc=loc, scale=scale, size=size)


def save_capacity_change_graph(df, start_year=None, end_year=None, output_file=None):
    # Filter the dataframe for the desired years if provided
    if start_year is not None:
        df = df[df["year"] >= start_year]
    if end_year is not None:
        df = df[df["year"] <= end_year]

        # Define the color mapping
    color_mapping = {
        "NGCCGrowth": "#000000",  # black
        "WindGrowth": "#0000FF",  # blue
        "NuclearGrowth": "#5F9EA0",  # cadetblue
        "PetroleumGrowth": "#FF8C00",  # darkorange1
        "NGSTGrowth": "#FF1493",  # deeppink
        "fusionGrowth": "#008000",  # green4
        "NGCTGrowth": "#9932CC",  # darkorchid
        "PVGrowth": "#9370DB",  # mediumpurple1
        "HydroGrowth": "#eea2ad",  # lightpink2
        "CoalGrowth": "#8b3a3a",  # maroon4
    }

    # Melt the dataframe for plotnine compatibility
    melted_df = pd.melt(
        df,
        id_vars=["year"],
        value_vars=color_mapping.keys(),
        var_name="growth_type",
        value_name="value",
    )

    # Create the plot
    p = (
        ggplot(melted_df)
        + geom_line(aes(x="year", y="value", color="growth_type"))
        + scale_color_manual(name="", values=color_mapping)
        + ggtitle("Capacity change by Type of Plant")
        + theme_minimal()
    )

    if output_file:
        p.save(output_file)
