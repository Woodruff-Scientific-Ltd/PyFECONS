"""
Comprehensive tests for MFE (Magnetic Fusion Energy) costing calculations.

This module tests the full MFE costing pipeline using the actual DefineInputs.py configurations
from the customers directory, ensuring tests use the same parameters as production.
"""

import os
import sys

import pytest

from pyfecons import RunCosting
from pyfecons.enums import ReactorType
from pyfecons.units import M_USD


def load_mfe_inputs():
    """Load MFE inputs from the actual DefineInputs.py file used in production."""
    # Add the customer directory to the path
    customer_dir = os.path.join(
        os.path.dirname(__file__), "..", "customers", "CATF", "mfe"
    )
    customer_dir = os.path.abspath(customer_dir)
    sys.path.insert(0, customer_dir)

    try:
        # Force reload of the module to avoid caching issues
        import importlib

        if "DefineInputs" in sys.modules:
            importlib.reload(sys.modules["DefineInputs"])
        else:
            import DefineInputs
        return DefineInputs.Generate()
    finally:
        # Clean up the path and module cache
        if customer_dir in sys.path:
            sys.path.remove(customer_dir)
        if "DefineInputs" in sys.modules:
            del sys.modules["DefineInputs"]


def test_mfe_tokamak_full_costing():
    """Test complete MFE tokamak costing calculation pipeline using production DefineInputs.py."""
    inputs = load_mfe_inputs()

    # Run the full costing calculation
    costing_data = RunCosting(inputs)

    # Validate that costing_data was created successfully
    assert costing_data is not None
    assert costing_data.reactor_type == ReactorType.MFE

    # Check that major cost categories were calculated
    assert hasattr(costing_data, "cas10")  # Pre-construction costs
    assert hasattr(costing_data, "cas21")  # Building costs
    assert hasattr(costing_data, "cas22")  # Reactor plant equipment
    assert hasattr(costing_data, "cas23")  # Turbine plant equipment
    assert hasattr(costing_data, "cas24")  # Electric plant equipment

    # Check that reactor equipment costs exist and are reasonable
    assert hasattr(costing_data.cas22, "C220100")  # Total reactor plant equipment
    reactor_equipment_cost = costing_data.cas22.C220100
    assert isinstance(reactor_equipment_cost, M_USD)
    assert reactor_equipment_cost > M_USD(0)  # Should be positive
    assert reactor_equipment_cost < M_USD(1000000)  # Should be reasonable (< $1T)

    # Check power table and LCOE
    assert hasattr(costing_data, "power_table")
    assert hasattr(costing_data, "lcoe")

    print(f"MFE Tokamak - Reactor Equipment Cost: ${reactor_equipment_cost:.2f}M")
    print(f"MFE Tokamak - LCOE: {costing_data.lcoe}")


def test_mfe_mirror_full_costing():
    """Test complete MFE mirror costing calculation pipeline."""
    inputs = load_mfe_inputs()  # Use same MFE config for now

    # Run the full costing calculation
    costing_data = RunCosting(inputs)

    # Validate that costing_data was created successfully
    assert costing_data is not None
    assert costing_data.reactor_type == ReactorType.MFE

    # Check that major cost categories were calculated
    assert hasattr(costing_data, "cas10")
    assert hasattr(costing_data, "cas21")
    assert hasattr(costing_data, "cas22")
    assert hasattr(costing_data, "cas23")
    assert hasattr(costing_data, "cas24")

    # Check reactor equipment costs
    assert hasattr(costing_data.cas22, "C220100")  # Total reactor plant equipment
    reactor_equipment_cost = costing_data.cas22.C220100
    assert isinstance(reactor_equipment_cost, M_USD)
    assert reactor_equipment_cost > M_USD(0)
    assert reactor_equipment_cost < M_USD(1000000)

    # Check power table and LCOE
    assert hasattr(costing_data, "power_table")
    assert hasattr(costing_data, "lcoe")

    print(f"MFE Mirror - Reactor Equipment Cost: ${reactor_equipment_cost:.2f}M")
    print(f"MFE Mirror - LCOE: {costing_data.lcoe}")


def test_mfe_costing_data_structure():
    """Test that MFE costing data has expected structure and all major components."""
    inputs = load_mfe_inputs()
    costing_data = RunCosting(inputs)

    # Test that all major CAS categories exist
    expected_cas_attributes = [
        "cas10",  # Pre-construction
        "cas21",  # Buildings
        "cas22",  # Reactor plant equipment
        "cas23",  # Turbine plant equipment
        "cas24",  # Electric plant equipment
        "cas25",  # Miscellaneous plant equipment
        "cas26",  # Heat rejection system
        "cas27",  # Special materials
        "cas28",  # Digital twin
        "cas29",  # Contingency
        "cas30",  # Capitalized indirect services
        "cas40",  # Capitalized owner costs
        "cas50",  # Capitalized supplementary costs
        "cas60",  # Capitalized financial costs
        "cas70",  # Annualized O&M
        "cas80",  # Annualized fuel
        "cas90",  # Annualized financial
    ]

    for attr in expected_cas_attributes:
        assert hasattr(costing_data, attr), f"Missing {attr} in costing data"
        assert getattr(costing_data, attr) is not None, f"{attr} is None"

    # Test that CAS 22 has the main total cost
    assert hasattr(
        costing_data.cas22, "C220100"
    ), "Missing C220100 (total reactor plant equipment) in CAS22"
    assert hasattr(
        costing_data.cas22, "C220000"
    ), "Missing C220000 (total CAS22) in CAS22"

    print("MFE costing data structure validation passed")


def test_mfe_cost_reasonableness():
    """Test that MFE costs are within reasonable ranges."""
    inputs = load_mfe_inputs()
    costing_data = RunCosting(inputs)

    # Test total capital cost is reasonable (should be billions, not trillions)
    # Note: All costs are in M_USD (millions of dollars)
    total_capital = (
        costing_data.cas10.C100000
        + costing_data.cas21.C210000
        + costing_data.cas22.C220000
        + costing_data.cas23.C230000
        + costing_data.cas24.C240000
        + costing_data.cas25.C250000
        + costing_data.cas26.C260000
        + costing_data.cas27.C270000
        + costing_data.cas28.C280000
        + costing_data.cas29.C290000
    )

    assert total_capital > M_USD(1000), "Total capital cost seems too low (< $1B)"
    assert total_capital < M_USD(100000), "Total capital cost seems too high (> $100B)"

    # Test that reactor equipment is a significant portion but not overwhelming
    reactor_cost = costing_data.cas22.C220100
    reactor_fraction = reactor_cost / total_capital
    assert reactor_fraction > 0.05, "Reactor equipment should be > 5% of total"
    assert (
        reactor_fraction < 0.95
    ), "Reactor equipment should be < 95% of total (allows for high-tech reactor configs)"

    print(f"Total capital cost: ${total_capital:.0f}M (${total_capital/1000:.1f}B)")
    print(f"Reactor equipment fraction: {reactor_fraction:.1%}")


if __name__ == "__main__":
    # Run tests individually for debugging
    test_mfe_tokamak_full_costing()
    test_mfe_mirror_full_costing()
    test_mfe_costing_data_structure()
    test_mfe_cost_reasonableness()
    print("All MFE tests completed successfully!")
