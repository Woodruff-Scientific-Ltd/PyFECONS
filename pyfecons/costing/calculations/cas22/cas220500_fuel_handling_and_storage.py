from pyfecons.costing.calculations.conversions import inflation_2010_2024
from pyfecons.costing.categories.cas220500 import CAS2205
from pyfecons.inputs.fuel_handling import FuelHandling
from pyfecons.units import M_USD


def cas_2205_fuel_handling_and_storage_costs(fuel_handling: FuelHandling) -> CAS2205:
    # Cost Category 22.5 Fuel Handling and Storage
    cas2205 = CAS2205()
    cas2205 = compute_fuel_handling_and_storage_costs(fuel_handling, cas2205)
    return cas2205


def compute_fuel_handling_and_storage_costs(IN: FuelHandling, OUT: CAS2205) -> CAS2205:
    # ITER values from: Waganer, L., 2013. ARIES Cost Account Documentation. [pdf] San Diego: University of California,
    #   San Diego. Available at: https://cer.ucsd.edu/_files/publications/UCSD-CER-13-01.pdf  Pge 90.
    OUT.C2205010ITER = M_USD(20.465 * inflation_2010_2024)
    OUT.C2205020ITER = M_USD(7 * inflation_2010_2024)
    OUT.C2205030ITER = M_USD(22.511 * inflation_2010_2024)
    OUT.C2205040ITER = M_USD(9.76 * inflation_2010_2024)
    OUT.C2205050ITER = M_USD(22.826 * inflation_2010_2024)
    OUT.C2205060ITER = M_USD(47.542 * inflation_2010_2024)

    # ITER inflation cost
    OUT.C22050ITER = M_USD(
        OUT.C2205010ITER
        + OUT.C2205020ITER
        + OUT.C2205030ITER
        + OUT.C2205040ITER
        + OUT.C2205050ITER
        + OUT.C2205060ITER
    )
    OUT.C220501 = M_USD(OUT.C2205010ITER * IN.learning_tenth_of_a_kind)
    OUT.C220502 = M_USD(OUT.C2205020ITER * IN.learning_tenth_of_a_kind)
    OUT.C220503 = M_USD(OUT.C2205030ITER * IN.learning_tenth_of_a_kind)
    OUT.C220504 = M_USD(OUT.C2205040ITER * IN.learning_tenth_of_a_kind)
    OUT.C220505 = M_USD(OUT.C2205050ITER * IN.learning_tenth_of_a_kind)
    OUT.C220506 = M_USD(OUT.C2205060ITER * IN.learning_tenth_of_a_kind)
    # ITER inflation cost
    OUT.C220500 = M_USD(
        OUT.C220501
        + OUT.C220502
        + OUT.C220503
        + OUT.C220504
        + OUT.C220505
        + OUT.C220506
    )
    return OUT
