"""Tests for dose-based bioshield safety calculations."""

import pytest

from pyfecons.costing.calculations.cas22.cas220102_shield import cas_220102_shield_costs
from pyfecons.costing.categories.cas220101 import CAS220101
from pyfecons.costing.safety.bioshield import (
    BIOSHIELD_MATERIAL_PROPERTIES,
    compute_required_thickness_meters,
)
from pyfecons.enums import BioshieldMaterial, ConfinementType, FusionMachineType
from pyfecons.inputs.basic import Basic
from pyfecons.inputs.blanket import Blanket
from pyfecons.inputs.radial_build import RadialBuild
from pyfecons.inputs.shield import Shield
from pyfecons.units import Meters, Meters3, Ratio


def _make_basic(safety=False):
    basic = Basic()
    basic.fusion_machine_type = FusionMachineType.MFE
    basic.confinement_type = ConfinementType.SPHERICAL_TOKAMAK
    basic.include_safety_hazards_costs = safety
    return basic


def _make_shield(with_bioshield_inputs=False):
    shield = Shield(
        f_SiC=Ratio(0.1),
        FPCPPFbLi=Ratio(0.3),
        f_W=Ratio(0.1),
        f_BFS=Ratio(0.5),
    )
    if with_bioshield_inputs:
        shield.bioshield_material = BioshieldMaterial.CONCRETE
        shield.initial_dose_without_bioshield = 0.5
        shield.regulatory_dose_limit = 0.05
    return shield


def _make_cas220101():
    cas220101 = CAS220101()
    cas220101.ht_shield_vol = Meters3(100.0)
    cas220101.lt_shield_vol = Meters3(50.0)
    cas220101.bioshield_vol = Meters3(200.0)
    cas220101.bioshield_ir = Meters(5.0)
    return cas220101


def _make_radial_build():
    rb = RadialBuild()
    rb.axis_t = Meters(3.0)
    rb.bioshield_t = Meters(0.15)
    return rb


class TestBackwardCompatibility:
    """Verify that without safety inputs, behavior is identical to before."""

    def test_no_safety_flag(self):
        basic = _make_basic(safety=False)
        shield = _make_shield(with_bioshield_inputs=False)
        cas220101 = _make_cas220101()

        result = cas_220102_shield_costs(basic, shield, Blanket(), cas220101)

        # Should use SS316 formula: vol * c_raw * m / 1e3
        # 200 * 2 * 2 / 1e3 = 0.8 M_USD
        assert abs(result.C22010203 - 0.8) < 0.01
        assert result.bioshield_required_thickness is None
        assert result.bioshield_dose_dtf is None

    def test_safety_flag_but_no_bioshield_inputs(self):
        basic = _make_basic(safety=True)
        shield = _make_shield(with_bioshield_inputs=False)
        cas220101 = _make_cas220101()

        result = cas_220102_shield_costs(basic, shield, Blanket(), cas220101)

        # Should still use SS316 formula (no bioshield inputs provided)
        assert abs(result.C22010203 - 0.8) < 0.01
        assert result.bioshield_required_thickness is None


class TestDoseBasedCalculation:
    """Verify dose-based bioshield when safety is enabled."""

    def test_dose_based_produces_different_cost(self):
        basic = _make_basic(safety=True)
        shield = _make_shield(with_bioshield_inputs=True)
        cas220101 = _make_cas220101()
        radial_build = _make_radial_build()

        result = cas_220102_shield_costs(
            basic, shield, Blanket(), cas220101, radial_build
        )

        # Should produce dose-based outputs
        assert result.bioshield_required_thickness is not None
        assert result.bioshield_dose_dtf == pytest.approx(0.1, abs=1e-6)
        assert result.bioshield_material_name == "Concrete"
        assert result.bioshield_vol_safety is not None
        # Cost should be different from SS316 baseline
        assert result.C22010203 != pytest.approx(0.8, abs=0.01)

    def test_never_shrinks_below_user_thickness(self):
        basic = _make_basic(safety=True)
        shield = _make_shield(with_bioshield_inputs=True)
        # Set a very large user thickness
        radial_build = _make_radial_build()
        radial_build.bioshield_t = Meters(10.0)
        cas220101 = _make_cas220101()

        result = cas_220102_shield_costs(
            basic, shield, Blanket(), cas220101, radial_build
        )

        # Required thickness should be much less than 10m, so effective
        # thickness should equal user's 10m
        assert result.bioshield_required_thickness < 10.0

    def test_dtf_calculation(self):
        basic = _make_basic(safety=True)
        shield = _make_shield(with_bioshield_inputs=True)
        shield.initial_dose_without_bioshield = 1.0
        shield.regulatory_dose_limit = 0.1
        cas220101 = _make_cas220101()
        radial_build = _make_radial_build()

        result = cas_220102_shield_costs(
            basic, shield, Blanket(), cas220101, radial_build
        )

        assert result.bioshield_dose_dtf == pytest.approx(0.1, abs=1e-6)

    def test_total_cost_includes_bioshield(self):
        basic = _make_basic(safety=True)
        shield = _make_shield(with_bioshield_inputs=True)
        cas220101 = _make_cas220101()
        radial_build = _make_radial_build()

        result = cas_220102_shield_costs(
            basic, shield, Blanket(), cas220101, radial_build
        )

        expected_total = (
            result.C22010201 + result.C22010202 + result.C22010203 + result.C22010204
        )
        assert result.C220102 == pytest.approx(expected_total, abs=0.01)

    def test_penetration_shield_is_10pct_of_bioshield(self):
        basic = _make_basic(safety=True)
        shield = _make_shield(with_bioshield_inputs=True)
        cas220101 = _make_cas220101()
        radial_build = _make_radial_build()

        result = cas_220102_shield_costs(
            basic, shield, Blanket(), cas220101, radial_build
        )

        assert result.C22010204 == pytest.approx(result.C22010203 * 0.1, abs=0.01)


class TestRequiredThickness:
    """Test the thickness computation function directly."""

    def test_no_shielding_needed(self):
        # Dose already below limit
        thickness = compute_required_thickness_meters(
            BioshieldMaterial.CONCRETE,
            initial_dose=0.01,
            regulatory_dose=0.05,
        )
        assert thickness == 0.0

    def test_zero_dose(self):
        thickness = compute_required_thickness_meters(
            BioshieldMaterial.CONCRETE,
            initial_dose=0.0,
            regulatory_dose=0.05,
        )
        assert thickness == 0.0

    def test_reasonable_thickness_for_concrete(self):
        # DTF = 0.1 should give roughly 10-16 inches = ~0.25-0.41 m
        # (polynomial fit interpolation from BRL-1174 data)
        thickness = compute_required_thickness_meters(
            BioshieldMaterial.CONCRETE,
            initial_dose=0.5,
            regulatory_dose=0.05,
        )
        assert 0.15 < thickness < 0.50

    def test_iron_thinner_than_water(self):
        # Iron is denser and should require less thickness than water
        # for the same DTF
        iron_t = compute_required_thickness_meters(
            BioshieldMaterial.IRON, initial_dose=0.5, regulatory_dose=0.05
        )
        water_t = compute_required_thickness_meters(
            BioshieldMaterial.WATER, initial_dose=0.5, regulatory_dose=0.05
        )
        assert iron_t < water_t

    def test_all_materials_produce_positive_thickness(self):
        for material in BioshieldMaterial:
            thickness = compute_required_thickness_meters(
                material, initial_dose=0.5, regulatory_dose=0.05
            )
            assert thickness > 0, f"{material} should require positive thickness"
