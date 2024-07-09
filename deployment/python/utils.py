import numpy as np
from scipy.ndimage import uniform_filter1d
import matplotlib.pyplot as plt


def energyTWhToCarbonOutputKG(fleet_t, typeChars, percent_CCS):
    # Align indices and calculate carbon output
    BTUFuel = typeChars.loc[fleet_t['type'], 'BTUFuel/kWhelec'].values
    kgCO2 = typeChars.loc[fleet_t['type'], 'kgCO2perMMBTU'].values
    carbon = (fleet_t['energy'].values * BTUFuel * kgCO2 * 10 ** (-6) * 10 ** 9)
    carbon *= (1 - percent_CCS)

    # Adjust for initial carbon
    birthAdd = (fleet_t['age'] == 1).values
    initialCarbon = typeChars.loc[fleet_t['type'][birthAdd], 'initialCarbonPerMW'].values
    capacity = fleet_t['capacity'][birthAdd].values
    carbon[birthAdd] += initialCarbon * capacity

    return carbon


def capacityMWToEnergyTWh(fleet_t, typeChars):
    cap_factors = typeChars.loc[fleet_t['type'], 'CapFactor'].values
    return fleet_t['capacity'].values * cap_factors * 8760 / (10 ** 2 * 10 ** 6)


def kgToGTons(kgs):
    return kgs * 10 ** (-12)


def mav(x, n=5):
    return uniform_filter1d(x, size=n)


def s_curve(T_ADOPT, k, t):
    return k / (1 + np.exp((np.log(1 / 19) - np.log(19)) / T_ADOPT * (t - T_ADOPT)))


# State abbreviations and names mapping
state_abbrev = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming'
}


# Example of plotting S-curves
def plot_s_curves():
    x = np.arange(-25, 101)
    for T_ADOPT in [5, 10, 20, 30, 40, 50]:
        y = s_curve(T_ADOPT, 1, x)
        plt.plot(x, y, label=f'T_ADOPT={T_ADOPT}')

    plt.title("Sample S-curves")
    plt.ylabel("Percent Penetration")
    plt.ylim(0, 1)
    plt.xlabel("Time")
    plt.legend()
    plt.show()
