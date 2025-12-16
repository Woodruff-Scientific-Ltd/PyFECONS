"""
Individual Blanket Parameter Tests

This module tests each blanket parameter individually by cycling through all possible values
for one parameter while keeping others at default values. This provides good coverage
without the combinatorial explosion of testing all possible combinations.
"""

import importlib
import os
import sys
from dataclasses import replace

import pytest

from pyfecons import RunCosting
from pyfecons.enums import (
    BlanketFirstWall,
    BlanketNeutronMultiplier,
    BlanketPrimaryCoolant,
    BlanketSecondaryCoolant,
    BlanketStructure,
    BlanketType,
    FusionMachineType,
)
from pyfecons.inputs.all_inputs import AllInputs
from pyfecons.inputs.blanket import Blanket
from pyfecons.units import M_USD


def load_ife_inputs() -> AllInputs:
    """Load IFE inputs from the actual DefineInputs.py file used in production."""
    return _load_inputs_from_customer_dir("ife")


def load_mfe_inputs() -> AllInputs:
    """Load MFE inputs from the actual DefineInputs.py file used in production."""
    return _load_inputs_from_customer_dir("mfe")


def _load_inputs_from_customer_dir(fusion_machine_type: str) -> AllInputs:
    """
    Load inputs from a customer DefineInputs.py file.

    Args:
        fusion_machine_type: Either "ife" or "mfe"

    Returns:
        AllInputs object from the DefineInputs.Generate() function
    """
    # Add the customer directory to the path
    customer_dir = os.path.join(
        os.path.dirname(__file__), "..", "customers", "CATF", fusion_machine_type
    )
    customer_dir = os.path.abspath(customer_dir)
    sys.path.insert(0, customer_dir)

    try:
        # Force reload of the module to avoid caching issues
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


def create_inputs_with_blanket_combination(
    base_inputs: AllInputs,
    first_wall: BlanketFirstWall,
    blanket_type: BlanketType,
    primary_coolant: BlanketPrimaryCoolant,
    secondary_coolant: BlanketSecondaryCoolant,
    neutron_multiplier: BlanketNeutronMultiplier,
    structure: BlanketStructure,
) -> AllInputs:
    """
    Create a new AllInputs object with the specified blanket combination.

    Args:
        base_inputs: Base AllInputs object to modify
        first_wall: First wall material
        blanket_type: Type of blanket
        primary_coolant: Primary coolant type
        secondary_coolant: Secondary coolant type
        neutron_multiplier: Neutron multiplier material
        structure: Structural material

    Returns:
        New AllInputs object with modified blanket configuration
    """
    # Create a new blanket with the specified combination
    new_blanket = Blanket(
        first_wall=first_wall,
        blanket_type=blanket_type,
        primary_coolant=primary_coolant,
        secondary_coolant=secondary_coolant,
        neutron_multiplier=neutron_multiplier,
        structure=structure,
    )

    # Use dataclasses.replace to create a new AllInputs with modified blanket
    new_inputs = replace(base_inputs, blanket=new_blanket)

    return new_inputs


class TestIFEBlanketParameters:
    """Test each IFE blanket parameter individually."""

    def get_default_blanket_params(self):
        """Get default blanket parameters from IFE DefineInputs."""
        inputs = load_ife_inputs()
        return (
            inputs.blanket.first_wall,
            inputs.blanket.blanket_type,
            inputs.blanket.primary_coolant,
            inputs.blanket.secondary_coolant,
            inputs.blanket.neutron_multiplier,
            inputs.blanket.structure,
        )

    @pytest.mark.parametrize("first_wall", list(BlanketFirstWall))
    def test_ife_first_wall_parameter(self, first_wall):
        """Test each first wall material for IFE."""
        base_inputs = load_ife_inputs()
        default_params = self.get_default_blanket_params()

        # Replace only the first_wall parameter
        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            first_wall,  # Test parameter
            default_params[1],  # blanket_type
            default_params[2],  # primary_coolant
            default_params[3],  # secondary_coolant
            default_params[4],  # neutron_multiplier
            default_params[5],  # structure
        )

        # Run costing and verify it completes
        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.IFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"IFE FirstWall {first_wall.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )

    @pytest.mark.parametrize("blanket_type", list(BlanketType))
    def test_ife_blanket_type_parameter(self, blanket_type):
        """Test each blanket type for IFE."""
        base_inputs = load_ife_inputs()
        default_params = self.get_default_blanket_params()

        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            default_params[0],  # first_wall
            blanket_type,  # Test parameter
            default_params[2],  # primary_coolant
            default_params[3],  # secondary_coolant
            default_params[4],  # neutron_multiplier
            default_params[5],  # structure
        )

        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.IFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"IFE BlanketType {blanket_type.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )

    @pytest.mark.parametrize("primary_coolant", list(BlanketPrimaryCoolant))
    def test_ife_primary_coolant_parameter(self, primary_coolant):
        """Test each primary coolant for IFE."""
        base_inputs = load_ife_inputs()
        default_params = self.get_default_blanket_params()

        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            default_params[0],  # first_wall
            default_params[1],  # blanket_type
            primary_coolant,  # Test parameter
            default_params[3],  # secondary_coolant
            default_params[4],  # neutron_multiplier
            default_params[5],  # structure
        )

        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.IFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"IFE PrimaryCoolant {primary_coolant.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )

    @pytest.mark.parametrize("secondary_coolant", list(BlanketSecondaryCoolant))
    def test_ife_secondary_coolant_parameter(self, secondary_coolant):
        """Test each secondary coolant for IFE."""
        base_inputs = load_ife_inputs()
        default_params = self.get_default_blanket_params()

        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            default_params[0],  # first_wall
            default_params[1],  # blanket_type
            default_params[2],  # primary_coolant
            secondary_coolant,  # Test parameter
            default_params[4],  # neutron_multiplier
            default_params[5],  # structure
        )

        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.IFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"IFE SecondaryCoolant {secondary_coolant.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )

    @pytest.mark.parametrize("neutron_multiplier", list(BlanketNeutronMultiplier))
    def test_ife_neutron_multiplier_parameter(self, neutron_multiplier):
        """Test each neutron multiplier for IFE."""
        base_inputs = load_ife_inputs()
        default_params = self.get_default_blanket_params()

        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            default_params[0],  # first_wall
            default_params[1],  # blanket_type
            default_params[2],  # primary_coolant
            default_params[3],  # secondary_coolant
            neutron_multiplier,  # Test parameter
            default_params[5],  # structure
        )

        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.IFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"IFE NeutronMultiplier {neutron_multiplier.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )

    @pytest.mark.parametrize("structure", list(BlanketStructure))
    def test_ife_structure_parameter(self, structure):
        """Test each structure material for IFE."""
        base_inputs = load_ife_inputs()
        default_params = self.get_default_blanket_params()

        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            default_params[0],  # first_wall
            default_params[1],  # blanket_type
            default_params[2],  # primary_coolant
            default_params[3],  # secondary_coolant
            default_params[4],  # neutron_multiplier
            structure,  # Test parameter
        )

        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.IFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"IFE Structure {structure.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )


class TestMFEBlanketParameters:
    """Test each MFE blanket parameter individually."""

    def get_default_blanket_params(self):
        """Get default blanket parameters from MFE DefineInputs."""
        inputs = load_mfe_inputs()
        return (
            inputs.blanket.first_wall,
            inputs.blanket.blanket_type,
            inputs.blanket.primary_coolant,
            inputs.blanket.secondary_coolant,
            inputs.blanket.neutron_multiplier,
            inputs.blanket.structure,
        )

    @pytest.mark.parametrize("first_wall", list(BlanketFirstWall))
    def test_mfe_first_wall_parameter(self, first_wall):
        """Test each first wall material for MFE."""
        base_inputs = load_mfe_inputs()
        default_params = self.get_default_blanket_params()

        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            first_wall,  # Test parameter
            default_params[1],  # blanket_type
            default_params[2],  # primary_coolant
            default_params[3],  # secondary_coolant
            default_params[4],  # neutron_multiplier
            default_params[5],  # structure
        )

        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.MFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"MFE FirstWall {first_wall.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )

    @pytest.mark.parametrize("blanket_type", list(BlanketType))
    def test_mfe_blanket_type_parameter(self, blanket_type):
        """Test each blanket type for MFE."""
        base_inputs = load_mfe_inputs()
        default_params = self.get_default_blanket_params()

        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            default_params[0],  # first_wall
            blanket_type,  # Test parameter
            default_params[2],  # primary_coolant
            default_params[3],  # secondary_coolant
            default_params[4],  # neutron_multiplier
            default_params[5],  # structure
        )

        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.MFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"MFE BlanketType {blanket_type.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )

    @pytest.mark.parametrize("primary_coolant", list(BlanketPrimaryCoolant))
    def test_mfe_primary_coolant_parameter(self, primary_coolant):
        """Test each primary coolant for MFE."""
        base_inputs = load_mfe_inputs()
        default_params = self.get_default_blanket_params()

        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            default_params[0],  # first_wall
            default_params[1],  # blanket_type
            primary_coolant,  # Test parameter
            default_params[3],  # secondary_coolant
            default_params[4],  # neutron_multiplier
            default_params[5],  # structure
        )

        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.MFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"MFE PrimaryCoolant {primary_coolant.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )

    @pytest.mark.parametrize("secondary_coolant", list(BlanketSecondaryCoolant))
    def test_mfe_secondary_coolant_parameter(self, secondary_coolant):
        """Test each secondary coolant for MFE."""
        base_inputs = load_mfe_inputs()
        default_params = self.get_default_blanket_params()

        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            default_params[0],  # first_wall
            default_params[1],  # blanket_type
            default_params[2],  # primary_coolant
            secondary_coolant,  # Test parameter
            default_params[4],  # neutron_multiplier
            default_params[5],  # structure
        )

        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.MFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"MFE SecondaryCoolant {secondary_coolant.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )

    @pytest.mark.parametrize("neutron_multiplier", list(BlanketNeutronMultiplier))
    def test_mfe_neutron_multiplier_parameter(self, neutron_multiplier):
        """Test each neutron multiplier for MFE."""
        base_inputs = load_mfe_inputs()
        default_params = self.get_default_blanket_params()

        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            default_params[0],  # first_wall
            default_params[1],  # blanket_type
            default_params[2],  # primary_coolant
            default_params[3],  # secondary_coolant
            neutron_multiplier,  # Test parameter
            default_params[5],  # structure
        )

        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.MFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"MFE NeutronMultiplier {neutron_multiplier.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )

    @pytest.mark.parametrize("structure", list(BlanketStructure))
    def test_mfe_structure_parameter(self, structure):
        """Test each structure material for MFE."""
        base_inputs = load_mfe_inputs()
        default_params = self.get_default_blanket_params()

        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            default_params[0],  # first_wall
            default_params[1],  # blanket_type
            default_params[2],  # primary_coolant
            default_params[3],  # secondary_coolant
            default_params[4],  # neutron_multiplier
            structure,  # Test parameter
        )

        costing_data = RunCosting(test_inputs)

        assert costing_data is not None
        assert costing_data.fusion_machine_type == FusionMachineType.MFE
        assert isinstance(costing_data.cas22.C220100, M_USD)
        assert costing_data.cas22.C220100 > M_USD(0)

        print(
            f"MFE Structure {structure.display_name}: ${costing_data.cas22.C220100:.2f}M"
        )


def test_parameter_counts():
    """Verify we're testing the expected number of parameters."""
    expected_counts = {
        "BlanketFirstWall": len(list(BlanketFirstWall)),
        "BlanketType": len(list(BlanketType)),
        "BlanketPrimaryCoolant": len(list(BlanketPrimaryCoolant)),
        "BlanketSecondaryCoolant": len(list(BlanketSecondaryCoolant)),
        "BlanketNeutronMultiplier": len(list(BlanketNeutronMultiplier)),
        "BlanketStructure": len(list(BlanketStructure)),
    }

    total_tests_per_reactor = sum(expected_counts.values())
    total_tests = total_tests_per_reactor * 2  # IFE + MFE

    print(f"Parameter counts: {expected_counts}")
    print(f"Total parameter tests per reactor: {total_tests_per_reactor}")
    print(f"Total parameter tests (IFE + MFE): {total_tests}")

    # Verify we have reasonable numbers
    assert (
        total_tests_per_reactor > 20
    ), "Should have at least 20 parameter tests per reactor"
    assert (
        total_tests_per_reactor < 50
    ), "Should have less than 50 parameter tests per reactor"


if __name__ == "__main__":
    # Run a quick test to verify functionality
    print("Testing IFE primary coolant parameters...")

    base_inputs = load_ife_inputs()
    default_params = (
        base_inputs.blanket.first_wall,
        base_inputs.blanket.blanket_type,
        base_inputs.blanket.primary_coolant,
        base_inputs.blanket.secondary_coolant,
        base_inputs.blanket.neutron_multiplier,
        base_inputs.blanket.structure,
    )

    for coolant in list(BlanketPrimaryCoolant)[:3]:  # Test first 3
        test_inputs = create_inputs_with_blanket_combination(
            base_inputs,
            default_params[0],
            default_params[1],
            coolant,
            default_params[3],
            default_params[4],
            default_params[5],
        )
        costing_data = RunCosting(test_inputs)
        print(f"  {coolant.display_name}: ${costing_data.cas22.C220100:.2f}M")

    print("Individual parameter testing works!")
