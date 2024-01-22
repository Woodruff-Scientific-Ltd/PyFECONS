
materials = {
    "FS": {"rho": 7470, "c_raw": 10, "m": 3, "sigma": 450},
    "Pb": {"rho": 9400, "c_raw": 2.4, "m": 1.5},
    "Li4SiO4": {"rho": 2390, "c_raw": 1, "m": 2},
    "Flibe": {"rho": 1900, "c": 40},
    "W": {"rho": 19300, "c_raw": 100, "m": 3},
    "Li": {"rho": 534, "c_raw": 70, "m": 1.5},
    "BFS": {"rho": 7800, "c_raw": 30, "m": 2},
    "PbLi": {"rho": None, "c": None},  # To be calculated
    "SiC": {"rho": 3200, "c_raw": 14.49, "m": 3},
    "Inconel": {"rho": 8440, "c_raw": 46, "m": 3},
    "Cu": {"rho": 7300, "c_raw": 10.2, "m": 3},
    "Polyimide": {"rho": 1430, "c_raw": 100, "m": 3},
    "YBCO": {"rho": 6200, "c": 55},
    "Concrete": {"rho": 2300, "c_raw": 13/25, "m": 2},
    "SS316": {"rho": 7860, "c_raw": 2, "m": 2, "sigma": 900},
    "Nb3Sn": {"c": 5},
    "Incoloy": {"rho": 8170, "c_raw": 4, "m": 2},
    "GdBCO": {},  # Density and cost not provided
    "He": {},  # Density and cost not provided
    "NbTi": {},  # Density and cost not provided
}

pblir = 10
materials["PbLi"]["rho"] = (materials["Pb"]["rho"] * pblir + materials["Li"]["rho"]) / (pblir + 1)
materials["PbLi"]["c"] = (materials["Pb"]["c_raw"] * materials["Pb"]["m"] * pblir + materials["Li"]["c_raw"] * materials["Li"]["m"]) / (pblir + 1)