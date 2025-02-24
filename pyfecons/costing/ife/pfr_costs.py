import matplotlib
from io import BytesIO
from matplotlib import pyplot as plt
from pyfecons.costing.calculations.interpolation import interpolate_plot

matplotlib.use("Agg")


yearlytcost_pfr_coords = [
    [4.948453608247423, 39.160839160839174],
    [6.892488954344623, 50.349650349650375],
    [9.013254786450663, 61.53846153846155],
    [11.045655375552284, 73.28671328671331],
    [12.989690721649483, 83.91608391608395],
    [15.022091310751103, 94.54545454545456],
    [16.966126656848303, 105.73426573426576],
    [18.954344624447714, 118.04195804195807],
    [20.898379970544916, 129.79020979020981],
    [22.930780559646536, 139.30069930069934],
    [24.963181148748156, 151.04895104895107],
]

pertarget_pfr_coords = [
    [4.9327354260089695, 0.25636363636363635],
    [6.95067264573991, 0.23454545454545453],
    [8.968609865470853, 0.21818181818181814],
    [10.986547085201797, 0.21363636363636362],
    [13.004484304932737, 0.20590909090909087],
    [14.977578475336328, 0.20181818181818179],
    [16.99551569506727, 0.19909090909090907],
    [18.968609865470853, 0.19545454545454544],
    [21.031390134529147, 0.19499999999999998],
    [23.00448430493274, 0.1927272727272727],
    [24.97757847533633, 0.19136363636363635],
]


def plot_target_pfr() -> bytes:
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
