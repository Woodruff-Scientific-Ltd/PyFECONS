from pyfecons.units import MW, M_USD


def compute_other_plant_equipment_costs(p_net: MW) -> M_USD:
    # from Waganer, L., 2013. ARIES Cost Account Documentation. [pdf] San Diego: University of California, San Diego.
    #   Available at: https://cer.ucsd.edu/_files/publications/UCSD-CER-13-01.pdf
    return M_USD(11.5 * (p_net / 1000) ** 0.8)
