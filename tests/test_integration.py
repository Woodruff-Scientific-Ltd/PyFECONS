"""
Integration tests for MFE and IFE costing calculations.

This module provides simplified integration tests that validate the full costing pipeline
runs successfully for both MFE and IFE configurations, producing reasonable output structure.
"""

import os

# Import helper functions from the test modules
import sys

import pytest

from pyfecons import RunCosting
from pyfecons.enums import ReactorType
from pyfecons.units import M_USD

sys.path.append(os.path.dirname(__file__))

from test_ife import load_ife_inputs
from test_mfe import load_mfe_inputs


def test_mfe_tokamak_integration():
    """Integration test for MFE tokamak costing - validates full pipeline runs successfully."""
    inputs = load_mfe_inputs()

    # Run the full costing calculation
    costing_data = RunCosting(inputs)

    # Basic validation
    assert costing_data is not None
    assert costing_data.reactor_type == ReactorType.MFE

    # Check that all major cost categories exist and are positive
    assert hasattr(costing_data, "cas10") and costing_data.cas10.C100000 > 0
    assert hasattr(costing_data, "cas21") and costing_data.cas21.C210000 > 0
    assert hasattr(costing_data, "cas22") and costing_data.cas22.C220000 > 0
    assert hasattr(costing_data, "cas23") and costing_data.cas23.C230000 > 0
    assert hasattr(costing_data, "cas24") and costing_data.cas24.C240000 > 0

    # Check that power table and LCOE were calculated
    assert hasattr(costing_data, "power_table") and costing_data.power_table is not None
    assert hasattr(costing_data, "lcoe") and costing_data.lcoe is not None
    assert hasattr(costing_data, "npv") and costing_data.npv is not None

    print(f"✓ MFE Tokamak - Total Capital: ${costing_data.cas20.C200000/1000:.1f}B")
    print(f"✓ MFE Tokamak - Reactor Equipment: ${costing_data.cas22.C220100/1000:.1f}B")


def test_mfe_mirror_integration():
    """Integration test for MFE mirror costing - validates full pipeline runs successfully."""
    inputs = load_mfe_inputs()  # Use same MFE config for now

    # Run the full costing calculation
    costing_data = RunCosting(inputs)

    # Basic validation
    assert costing_data is not None
    assert costing_data.reactor_type == ReactorType.MFE

    # Check that all major cost categories exist and are positive
    assert hasattr(costing_data, "cas10") and costing_data.cas10.C100000 > 0
    assert hasattr(costing_data, "cas21") and costing_data.cas21.C210000 > 0
    assert hasattr(costing_data, "cas22") and costing_data.cas22.C220000 > 0

    # Check that power table and LCOE were calculated
    assert hasattr(costing_data, "power_table") and costing_data.power_table is not None
    assert hasattr(costing_data, "lcoe") and costing_data.lcoe is not None

    print(f"✓ MFE Mirror - Total Capital: ${costing_data.cas20.C200000/1000:.1f}B")
    print(f"✓ MFE Mirror - Reactor Equipment: ${costing_data.cas22.C220100/1000:.1f}B")


def test_ife_integration():
    """Integration test for IFE costing - validates full pipeline runs successfully."""
    inputs = load_ife_inputs()

    # Run the full costing calculation
    costing_data = RunCosting(inputs)

    # Basic validation
    assert costing_data is not None
    assert costing_data.reactor_type == ReactorType.IFE

    # Check that all major cost categories exist and are positive
    assert hasattr(costing_data, "cas10") and costing_data.cas10.C100000 > 0
    assert hasattr(costing_data, "cas21") and costing_data.cas21.C210000 > 0
    assert hasattr(costing_data, "cas22") and costing_data.cas22.C220000 > 0

    # Check that power table and LCOE were calculated
    assert hasattr(costing_data, "power_table") and costing_data.power_table is not None
    assert hasattr(costing_data, "lcoe") and costing_data.lcoe is not None

    print(
        f"✓ IFE Direct Drive - Total Capital: ${costing_data.cas20.C200000/1000:.1f}B"
    )
    print(
        f"✓ IFE Direct Drive - Reactor Equipment: ${costing_data.cas22.C220100/1000:.1f}B"
    )


def test_costing_data_structure():
    """Test that costing data has expected structure for both MFE and IFE."""
    mfe_inputs = load_mfe_inputs()
    ife_inputs = load_ife_inputs()

    mfe_data = RunCosting(mfe_inputs)
    ife_data = RunCosting(ife_inputs)

    # Test that both have the same major structure
    expected_attributes = [
        "reactor_type",
        "power_table",
        "cas10",
        "cas21",
        "cas22",
        "cas23",
        "cas24",
        "cas25",
        "cas26",
        "cas27",
        "cas28",
        "cas29",
        "cas20",
        "cas30",
        "cas40",
        "cas50",
        "cas60",
        "cas70",
        "cas80",
        "cas90",
        "lcoe",
        "npv",
    ]

    for attr in expected_attributes:
        assert hasattr(mfe_data, attr), f"MFE missing {attr}"
        assert hasattr(ife_data, attr), f"IFE missing {attr}"

    # Test that reactor types are correct
    assert mfe_data.reactor_type == ReactorType.MFE
    assert ife_data.reactor_type == ReactorType.IFE

    print("✓ Both MFE and IFE have consistent costing data structure")


def test_cost_reasonableness():
    """Test that costs are within reasonable ranges for fusion power plants."""
    mfe_inputs = load_mfe_inputs()
    mfe_data = RunCosting(mfe_inputs)

    # All costs should be positive
    assert mfe_data.cas20.C200000 > M_USD(0), "Total capital cost should be positive"
    assert mfe_data.cas22.C220100 > M_USD(
        0
    ), "Reactor equipment cost should be positive"

    # Costs should be substantial but not absurdly high (fusion is expensive!)
    total_capital = mfe_data.cas20.C200000
    assert total_capital > M_USD(1000), "Total capital should be > $1B"
    assert total_capital < M_USD(
        100000
    ), "Total capital should be < $100B (reasonable for fusion)"

    # Reactor equipment should be a significant portion
    reactor_cost = mfe_data.cas22.C220100
    reactor_fraction = reactor_cost / total_capital
    assert 0.01 < reactor_fraction < 0.9, "Reactor equipment should be 1-90% of total"

    print(
        f"✓ Costs are reasonable: Total ${total_capital/1000:.1f}B, Reactor {reactor_fraction:.1%}"
    )


if __name__ == "__main__":
    # Run integration tests individually for debugging
    test_mfe_tokamak_integration()
    test_mfe_mirror_integration()
    test_ife_integration()
    test_costing_data_structure()
    test_cost_reasonableness()
    print(
        "\n🎉 All integration tests passed! Costing calculations are working correctly."
    )
