# placeholder file to test the testing capability

import pytest

from pyfecons import compute_cas22_reactor_equipment_total_cost
from pyfecons.enums import (
    ReactorType,
    ConfinementType,
    BlanketFirstWall,
    BlanketType,
    BlanketPrimaryCoolant,
    BlanketSecondaryCoolant,
    BlanketNeutronMultiplier,
    BlanketStructure,
)
from pyfecons.inputs import Blanket, RadialBuild
from pyfecons.units import Ratio, Meters


def test_mfe_tokamak():
    blanket = Blanket(
        BlanketFirstWall.BERYLLIUM,
        BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI4SIO4,
        BlanketPrimaryCoolant.DUAL_COOLANT_PBLI_AND_HE,
        BlanketSecondaryCoolant.LITHIUM_LI,
        BlanketNeutronMultiplier.NONE,
        BlanketStructure.STAINLESS_STEEL_SS,
    )
    radial_build = RadialBuild(
        elon=Ratio(3),
        axis_t=Meters(3),
        plasma_t=Meters(1.1),
        vacuum_t=Meters(0.1),
        firstwall_t=Meters(0.2),
        blanket1_t=Meters(0.8),
        reflector_t=Meters(0.2),
        ht_shield_t=Meters(0.2),
        structure_t=Meters(0.2),
        gap1_t=Meters(0.5),
        vessel_t=Meters(0.2),
        coil_t=Meters(0.25),
        gap2_t=Meters(0.5),
        lt_shield_t=Meters(0.3),
        bioshield_t=Meters(1),
    )
    result_cost = compute_cas22_reactor_equipment_total_cost(
        reactor_type=ReactorType.MFE,
        confinement_type=ConfinementType.SPHERICAL_TOKAMAK,
        radial_build=radial_build,
        blanket=blanket,
    )
    expected_result_cost = (
        9757.80  #! this could become deprecated if cost calculation changes
    )
    assert pytest.approx(result_cost, rel=1e-2) == expected_result_cost


def test_mfe_mirror():
    blanket = Blanket(
        BlanketFirstWall.BERYLLIUM,
        BlanketType.SOLID_FIRST_WALL_WITH_A_SOLID_BREEDER_LI4SIO4,
        BlanketPrimaryCoolant.DUAL_COOLANT_PBLI_AND_HE,
        BlanketSecondaryCoolant.LITHIUM_LI,
        BlanketNeutronMultiplier.NONE,
        BlanketStructure.STAINLESS_STEEL_SS,
    )
    radial_build = RadialBuild(
        chamber_length=Meters(12),
        axis_t=Meters(0),
        plasma_t=Meters(4.9),
        vacuum_t=Meters(0.1),
        firstwall_t=Meters(0.1),
        blanket1_t=Meters(1),
        reflector_t=Meters(0.1),
        ht_shield_t=Meters(0.25),
        structure_t=Meters(0.2),
        gap1_t=Meters(0.5),
        vessel_t=Meters(0.2),
        coil_t=Meters(1.76),
        gap2_t=Meters(1),
        lt_shield_t=Meters(0.3),
        bioshield_t=Meters(1),
    )
    result_cost = compute_cas22_reactor_equipment_total_cost(
        ReactorType.MFE, ConfinementType.MAGNETIC_MIRROR, blanket, radial_build
    )
    expected_result_cost = (
        1217.12  #! this could become deprecated if cost calculation changes
    )
    assert pytest.approx(result_cost, rel=1e-2) == expected_result_cost


def test_mfe_mirror_minimal():
    blanket = Blanket(
        BlanketFirstWall.BERYLLIUM,
        BlanketType.SOLID_FIRST_WALL_NO_BREEDER_ANEUTRONIC_FUEL,
        BlanketPrimaryCoolant.FLIBE,
        BlanketSecondaryCoolant.WATER,
        BlanketNeutronMultiplier.PB,
        BlanketStructure.OXIDE_DISPERSION_STRENGTHENED_ODS_STEEL,
    )
    radial_build = RadialBuild(
        chamber_length=Meters(10),
        axis_t=Meters(1),
        plasma_t=Meters(3),
        vacuum_t=Meters(0.2),
        firstwall_t=Meters(0.01),
        blanket1_t=Meters(1),
        reflector_t=Meters(0),
        ht_shield_t=Meters(0),
        structure_t=Meters(0),
        gap1_t=Meters(0),
        vessel_t=Meters(0),
        coil_t=Meters(0),
        gap2_t=Meters(0),
        lt_shield_t=Meters(0),
        bioshield_t=Meters(0),
    )
    result_cost = compute_cas22_reactor_equipment_total_cost(
        ReactorType.MFE, ConfinementType.MAGNETIC_MIRROR, blanket, radial_build
    )
    expected_result_cost = (
        84.315  #! this could become deprecated if cost calculation changes
    )
    assert pytest.approx(result_cost, rel=1e-2) == expected_result_cost
