"""Tests for rapid structural oxidation first wall coating calculations."""

import pytest

from pyfecons.costing.safety.oxidation import (
    coating_required,
    compute_coating_cost_usd,
    compute_fw_surface_area,
    compute_rci,
)
from pyfecons.enums import BlanketStructure, ConfinementType, FusionMachineType


class TestRci:
    """Test Relative Consequence Index calculation."""

    def test_fms_is_reference(self):
        # FMS (HT-9) is the reference case, RCI should be 1.0
        rci = compute_rci(BlanketStructure.FERRITIC_MARTENSITIC_STEEL_FMS)
        assert rci == pytest.approx(1.0)

    def test_ods_same_as_fms(self):
        rci = compute_rci(BlanketStructure.OXIDE_DISPERSION_STRENGTHENED_ODS_STEEL)
        assert rci == pytest.approx(1.0)

    def test_ss_worse_than_fms(self):
        # SS has smaller margin (560°C vs 950°C), RCI > 1
        rci = compute_rci(BlanketStructure.STAINLESS_STEEL_SS)
        assert rci > 1
        assert rci == pytest.approx(950 / 560, abs=0.01)

    def test_vanadium_much_worse(self):
        # Vanadium has tiny margin (100°C), RCI >> 1
        rci = compute_rci(BlanketStructure.VANADIUM)
        assert rci > 1
        assert rci == pytest.approx(9.5, abs=0.01)


class TestCoatingRequired:
    """Test coating trigger logic."""

    def test_fms_no_coating(self):
        rci = compute_rci(BlanketStructure.FERRITIC_MARTENSITIC_STEEL_FMS)
        assert not coating_required(rci)

    def test_ods_no_coating(self):
        rci = compute_rci(BlanketStructure.OXIDE_DISPERSION_STRENGTHENED_ODS_STEEL)
        assert not coating_required(rci)

    def test_ss_needs_coating(self):
        rci = compute_rci(BlanketStructure.STAINLESS_STEEL_SS)
        assert coating_required(rci)

    def test_vanadium_needs_coating(self):
        rci = compute_rci(BlanketStructure.VANADIUM)
        assert coating_required(rci)

    def test_negative_margin_needs_coating(self):
        # Negative RCI (T_lt < T_o) should trigger coating
        assert coating_required(-4.75)

    def test_rci_exactly_one_no_coating(self):
        assert not coating_required(1.0)


class TestSurfaceArea:
    """Test first wall surface area computation."""

    def test_ife_sphere(self):
        import math

        area = compute_fw_surface_area(
            FusionMachineType.IFE,
            ConfinementType.LASER_DRIVEN_DIRECT_DRIVE,
            firstwall_ir=5.0,
        )
        assert area == pytest.approx(4 * math.pi * 25, abs=1)

    def test_mirror_cylinder(self):
        import math

        area = compute_fw_surface_area(
            FusionMachineType.MFE,
            ConfinementType.MAGNETIC_MIRROR,
            firstwall_ir=2.0,
            chamber_length=10.0,
        )
        assert area == pytest.approx(2 * math.pi * 2.0 * 10.0, abs=1)

    def test_tokamak_torus(self):
        area = compute_fw_surface_area(
            FusionMachineType.MFE,
            ConfinementType.SPHERICAL_TOKAMAK,
            firstwall_ir=5.0,
            axis_t=3.0,
            elon=1.7,
        )
        # Should be a positive, reasonable area
        assert area > 0
        assert area > 100  # At least 100 m² for any reasonable tokamak


class TestCoatingCost:
    """Test coating cost calculation."""

    def test_notebook_values(self):
        # Notebook: 600 m², 2mm, tungsten
        # material = 600 * 0.002 * 19300 * 100 = $2,316,000
        # application = $2,316,000
        # R&D = $1,158,000
        # total = $5,790,000
        cost = compute_coating_cost_usd(600, 0.002, 1.0)
        assert cost == pytest.approx(5_790_000, rel=0.01)

    def test_zero_area(self):
        cost = compute_coating_cost_usd(0, 0.002, 1.0)
        assert cost == 0

    def test_higher_application_factor(self):
        base = compute_coating_cost_usd(600, 0.002, 1.0)
        higher = compute_coating_cost_usd(600, 0.002, 2.0)
        assert higher > base
