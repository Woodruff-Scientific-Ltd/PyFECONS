import os
import psutil
import numpy as np
from scipy.ndimage import uniform_filter1d
import matplotlib.pyplot as plt


def energyTWhToCarbonOutputKG(fleet_energy, fleet_type, typeChars, percent_CCS):
    BTUFuel = np.array([typeChars.loc[t, 'BTUFuel/kWhelec'] for t in fleet_type])
    kgCO2 = np.array([typeChars.loc[t, 'kgCO2perMMBTU'] for t in fleet_type])
    carbon = (fleet_energy * BTUFuel * kgCO2 * 10 ** (-6) * 10 ** 9)
    carbon *= (1 - percent_CCS)
    return carbon


def capacityMWToEnergyTWh(fleet_capacity, fleet_type, typeChars):
    cap_factors = np.array([typeChars.loc[t, 'CapFactor'] for t in fleet_type])
    return fleet_capacity * cap_factors * 8760 / (10 ** 2 * 10 ** 6)


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


def log_memory_usage(message):
    process = psutil.Process(os.getpid())
    print(f"Memory usage at {message}: {process.memory_info().rss / 1024 ** 2:.2f} MB")