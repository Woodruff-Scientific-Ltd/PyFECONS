# Rapid Structural Oxidation — First Wall Coating Implementation

Tracking document for implementing oxidation-driven first wall coating costs in PyFECONS (CAS 22.01.01).

Branch: `mfe-safety-part-ii` in PyFECONS

## Goal

When safety costs are enabled, evaluate whether the structural material's oxidation margin requires a protective tungsten first wall coating. If so, compute and add the coating cost to CAS 22.01.01. MFE and IFE. When safety is disabled, behavior is identical to today.

## Background

A fusion reactor's first wall operates in vacuum. If an oxidant (air) enters the plasma chamber — e.g., from a vacuum boundary breach — rapid structural oxidation can occur. The severity depends on the margin between the material's operating temperature and its oxidation onset temperature. If this margin is small (worse than the reference case HT-9), a protective tungsten coating is required.

Reference: Piet, Kazimi & Lidsky (1982), "Potential Consequences of Tokamak Fusion Reactor Accidents: The Materials Impact".

## New Inputs

Two new optional fields on `inputs/blanket.py` (or `inputs/shield.py`), only used when safety costs enabled:

| Field | Type | Default | Description |
|---|---|---|---|
| `fw_coating_thickness` | `Meters` (float) | `0.002` | Tungsten coating thickness (m). Default 2 mm per Cui et al. (2021). |
| `fw_application_cost_factor` | `float` | `1.0` | Application cost as fraction of material cost. Default 100% (plasma spray). |

The structural material and its oxidation properties are derived from the existing `blanket.structure` enum (`BlanketStructure`). No new enum needed.

## Cost Categories Affected

Only **CAS 22.01.01 (First Wall)** changes — coating cost is added when RCI < 1.

### Without safety (existing behavior, unchanged)
```
C22010101 = firstwall_vol × material.rho × material.c_raw × material.m
```

### With safety enabled
```
1. Map blanket.structure to oxidation properties:
     BlanketStructure          → T_o (°C)  → T_lt (°C)
     STAINLESS_STEEL_SS        → 450       → 1010
     FERRITIC_MARTENSITIC_STEEL → 450      → 1400
     ODS                       → 450       → 1400  (assumed same as FMS)
     VANADIUM                  → 600       → 700

2. Compute RCI = (T_lt(HT-9) - T_o(HT-9)) / (T_lt - T_o)
     Reference case: HT-9 margin = 1400 - 450 = 950°C
     RCI = 950 / (T_lt - T_o)

3. If RCI >= 1: no coating needed, C22010101 unchanged
   If RCI < 1: compute coating cost and ADD to C22010101

4. Coating cost:
     fw_surface_area = derived from first wall geometry (inner surface area)
     coating_vol = fw_surface_area × fw_coating_thickness
     material_cost = coating_vol × tungsten.rho × tungsten.c_raw
     application_cost = material_cost × fw_application_cost_factor
     rd_cost = material_cost × 0.5
     total_coating_cost = material_cost + application_cost + rd_cost

5. C22010101 = base_first_wall_cost + total_coating_cost
```

**Net effect:** For 316 SS (RCI = 950/560 = 1.70 ≥ 1), no coating. For Vanadium (RCI = 950/100 = 9.5 ≥ 1 — wait, this gives RCI > 1 too, meaning no coating. But the notebook says TZM is problematic because T_lt < T_o). The RCI formula triggers coating when the oxidation margin is *smaller* than HT-9's, i.e. RCI > 1 means worse margin. See assumption #2.

## Open Questions — Working Assumptions

---

### 1. RCI threshold and direction

**Problem:** The notebook formula `RCI = (T_lt(HT-9) - T_o(HT-9)) / (T_lt - T_o)` gives the *ratio* of HT-9's margin to the candidate material's margin. A larger RCI means the candidate has a *smaller* oxidation margin (worse). The notebook checks `if RCI < 1: coating needed`, which means coating is needed when the candidate has a *larger* margin than HT-9 — this seems inverted.

Looking at the data:
- HT-9: margin = 1400 - 450 = 950°C → RCI = 1.0 (reference)
- 316 SS: margin = 1010 - 450 = 560°C → RCI = 950/560 = 1.70 (worse margin, coating should be needed)
- Vanadium: margin = 700 - 600 = 100°C → RCI = 950/100 = 9.50 (much worse, coating needed)
- TZM: margin = 700 - 900 = -200°C → RCI = 950/(-200) = -4.75 (negative, T_lt < T_o, extremely dangerous)

**Assumption:** The correct threshold is `RCI > 1` (or RCI < 0 for negative margins). Coating is needed when the material's oxidation margin is smaller than HT-9's reference case. The notebook's `if RCI < 1` check appears to be an error — with 316 SS as default input, RCI = 1.70, so the notebook would skip coating, but 316 SS has a worse margin than HT-9.

We implement: **coating required when `RCI > 1` OR `RCI < 0`** (i.e., whenever the margin is worse than HT-9).

**ASK:** Is the RCI threshold `> 1` (worse margin than HT-9 triggers coating) or `< 1` (better margin triggers coating)? The notebook code and the physical reasoning seem contradictory. Please clarify the intent.

---

### 2. Structural material to oxidation temperature mapping

**Problem:** PyFECONS `BlanketStructure` enum values don't map 1:1 to the notebook's oxidation materials. The notebook has 316 SS, HT-9, Vanadium, TZM. PyFECONS has STAINLESS_STEEL_SS, FERRITIC_MARTENSITIC_STEEL_FMS, ODS, VANADIUM.

**Assumption:**

| BlanketStructure | Maps to | T_o (°C) | T_lt (°C) | Margin (°C) | Source |
|---|---|---|---|---|---|
| STAINLESS_STEEL_SS | 316 SS | 450 | 1010 | 560 | Notebook; Piet et al. (1982) |
| FERRITIC_MARTENSITIC_STEEL_FMS | HT-9 | 450 | 1400 | 950 | Notebook; Piet et al. (1982) |
| ODS | HT-9 (proxy) | 450 | 1400 | 950 | Assumed same as FMS — both ferritic |
| VANADIUM | Vanadium | 600 | 700 | 100 | Notebook; Piet et al. (1982) |

TZM (molybdenum alloy) is not in the current enum and is excluded. If added later, T_o=900, T_lt=700 (negative margin).

**ASK:** Is the ODS → HT-9 proxy reasonable? ODS steels are ferritic-based, so oxidation behavior should be similar. Also, should TZM be added to the enum?

---

### 3. First wall surface area

**Problem:** The notebook hardcodes 600 m² (ITER-like). PyFECONS computes `firstwall_vol` from geometry but not surface area directly.

**Assumption:** Derive surface area from the first wall inner radius and reactor geometry:
- MFE tokamak: `fw_surface_area = 2π × R × 2π × a_fw × κ` where R = axis_t (major radius), a_fw = firstwall_ir - axis_t (minor radius at first wall), κ = elongation. Simplified: `4π² × axis_t × (firstwall_ir - axis_t) × elon`.
- MFE mirror: `fw_surface_area = 2π × firstwall_ir × chamber_length` (cylinder).
- IFE: `fw_surface_area = 4π × firstwall_ir²` (sphere).

This is more accurate than a fixed value since it tracks the actual reactor geometry.

**ASK:** Is deriving surface area from the radial build preferred, or should we use a simpler fixed input (e.g. 600 m²)?

---

### 4. Coating cost model

**Problem:** The notebook uses: material cost + application (100% of material) + R&D (50% of material) = 2.5× raw material cost. PyFECONS has a manufacturing factor `m` for tungsten (m=3). These are different cost models.

**Assumption:** Use the notebook's explicit cost breakdown (not PyFECONS materials.W.m) since the coating process (plasma spray / aerosol deposition) is different from bulk tungsten component fabrication:
- Material cost: `coating_vol × W.rho × W.c_raw` (using W.c_raw = $100/kg)
- Application cost: 100% of material cost (default, overridable via input)
- R&D/QC cost: 50% of material cost (fixed)
- Total multiplier: 2.5× raw material cost

This gives a total of ~$5.8M for a 600 m², 2mm coating (consistent with notebook output).

**ASK:** Is 2.5× (material + 100% application + 50% R&D) reasonable for a FOAK plant? For NOAK, the R&D fraction could drop. Should we parameterize the R&D fraction too?

---

### 5. Coating thickness

**Problem:** Notebook uses 2 mm. Cui et al. (2021) demonstrated coatings up to 2 mm on steel substrates with good cycling performance (300-800°C, 50+ cycles).

**Assumption:** Default 2 mm, exposed as an input parameter (`fw_coating_thickness`) so it can be varied. The Cui et al. (2021) paper provides experimental validation at this thickness.

**ASK:** Is 2 mm appropriate for all reactor sizes, or should it scale with neutron wall loading or first wall heat flux?

---

### 6. MFE and IFE

**Problem:** The safety implementation status says "MFE only". However, the RCI calculation depends on structural material oxidation temperatures — a material property, not geometry-dependent. The only geometry-specific piece is first wall surface area, which PyFECONS already computes for IFE (spherical: `4π × firstwall_ir²`).

**Assumption:** Implement for both MFE and IFE. The oxidation concern is about the **structural material** (`BlanketStructure`: SS, FMS, ODS, Vanadium) — the load-bearing component that oxidizes catastrophically if air enters. This is independent of the first wall surface material (`BlanketFirstWall`) and independent of reactor geometry. The `BlanketStructure` enum and oxidation temperature mapping are shared between MFE and IFE. The coating cost formula (surface area × thickness × tungsten) just needs the appropriate surface area for each geometry.

**ASK:** Is there any IFE-specific reason to exclude oxidation analysis? The structural material oxidation physics applies equally in any vacuum-enclosed reactor.

---

### 7. Operating temperatures as inputs vs. fixed per material

**Problem:** The notebook hardcodes T_o and T_lt per structural material. In practice, operating temperature depends on the specific reactor design (coolant choice, power level, etc.).

**Assumption:** Fix T_o and T_lt per `BlanketStructure` enum value using the notebook's values. These are material properties, not design variables. The operating temperatures in the notebook (450°C for steels, 600°C for vanadium) are representative of fusion blanket conditions from BCSS (Abdou et al. 1983) and ESECOM (Logan, Holdren et al. 1988).

**ASK:** Should T_o be an input parameter (design-specific) while T_lt remains fixed (material property)?

## Files to Change

### New files
- `pyfecons/costing/safety/oxidation.py` — RCI calculation, coating cost logic, material oxidation properties

### Modified files
- `pyfecons/inputs/blanket.py` — Add optional fields: `fw_coating_thickness`, `fw_application_cost_factor`
- `pyfecons/costing/calculations/cas22/cas220101_reactor_equipment.py` — Add coating cost when safety enabled + RCI triggers
- `pyfecons/costing/categories/cas220101.py` — Add optional output fields for RCI and coating cost
- `pyfecons/costing/mfe/mfe.py` — Pass `basic` to cas220101 function (for safety flag check)
- `pyfecons/costing/ife/ife.py` — Same
- `pyfecons/report/sections/cas220101_section.py` — Conditional replacements for oxidation outputs
- `pyfecons/costing/mfe/templates/CAS220101_MFE_DT.tex` — `\ifsafetycosts` block for coating
- `pyfecons/costing/ife/templates/CAS220101_IFE_DT.tex` — Same
- `customers/CATF/mfe/DefineInputsSafety.py` — Add coating inputs
- `customers/CATF/ife/DefineInputsSafety.py` — Add coating inputs

### Tests
- `tests/test_oxidation_safety.py` — RCI calculation, coating cost, backward compat, edge cases

## Dependency Order

```
1. costing/safety/oxidation.py (new file: RCI + coating logic)
2. inputs/blanket.py (new optional fields)
3. costing/categories/cas220101.py (new output fields)
4. costing/calculations/cas22/cas220101_reactor_equipment.py (conditional branch)
5. costing/mfe/mfe.py (pass basic to cas220101)
6. report/sections/cas220101_section.py (conditional replacements)
7. templates CAS220101_MFE_DT.tex (conditional text)
8. DefineInputsSafety.py (add inputs)
9. Tests
```

## Progress

Implementation complete (2026-03-26).

- [x] Create implementation plan and document assumptions
- [x] Implement oxidation module (`costing/safety/oxidation.py`)
- [x] Modify cas220101 calculation (conditional coating cost)
- [x] Update report section and templates (MFE + IFE)
- [x] Update CATF DefineInputsSafety (MFE + IFE)
- [x] Write tests — 16 new tests, all 112 pass
- [x] Run all 8 report variants — all complete without error

### Outstanding

- [ ] Review assumptions with domain experts (see ASK items above)

### Notes

CATF default structure is FMS (HT-9 equivalent), so RCI = 1.0 and no coating is triggered. To see the coating cost in action, change `blanket.structure` to `STAINLESS_STEEL_SS` (RCI = 1.70) or `VANADIUM` (RCI = 9.50).
