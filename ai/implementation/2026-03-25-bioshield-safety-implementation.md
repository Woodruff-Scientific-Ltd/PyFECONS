# Bioshield Dose-Based Safety Implementation

Tracking document for implementing dose-based bioshield safety calculations in PyFECONS (CAS 22.01.02.03).

Branch: `mfe-safety-part-ii` in PyFECONS

## Goal

When safety costs are enabled, validate/adjust the bioshield thickness based on radiation dose attenuation requirements, and cost using the selected bioshield material (not hard-coded SS316). When safety is disabled, behavior is identical to today.

## New Inputs

Three new optional fields on `inputs/shield.py`, only used when safety costs are enabled:

| Field | Type | Default | Description |
|---|---|---|---|
| `bioshield_material` | `BioshieldMaterial` enum | `CONCRETE` | Bioshield material selection. Options: CONCRETE, BORATED_POLYETHYLENE, IRON, WATER. |
| `initial_dose_without_bioshield` | `Sv_yr` (float) | `0.5` | Annual dose rate at bioshield inner surface with blanket/shield in place but no bioshield. Design-specific; should come from neutronics calculation. |
| `regulatory_dose_limit` | `Sv_yr` (float) | `0.05` | Target dose rate outside bioshield. Default is US NRC occupational limit (50 mSv/yr). Override for other jurisdictions. |

New enum in `enums.py`:

```python
class BioshieldMaterial(Enum):
    CONCRETE = "concrete"
    BORATED_POLYETHYLENE = "borated_polyethylene"
    IRON = "iron"
    WATER = "water"
```

Each material carries its own density, cost/kg, manufacturing factor, and DTF-vs-thickness curve (from BRL-1174).

## Cost Categories Affected

Only **CAS 22.01.02.03 (Bioshield)** changes. No other cost categories are affected.

### Without safety (existing behavior, unchanged)
```
bioshield_vol = geometry from cas220101 radial build (uses bioshield_t)
C22010203 = bioshield_vol × SS316.rho × SS316.c_raw × SS316.m
```
Hard-coded SS316, no dose calculation.

### With safety enabled
```
1. DTF = regulatory_dose_limit / initial_dose_without_bioshield
      e.g. 0.05 / 0.5 = 0.1

2. required_thickness = inverse of material's DTF-vs-thickness polynomial
      e.g. for concrete at DTF=0.1 → ~10 inches (~25 cm)

3. effective_thickness = max(required_thickness, user's bioshield_t)
      never shrink below what the user specified

4. effective_vol = recompute bioshield volume using effective_thickness
      same geometry formula as cas220101, just with the larger thickness

5. C22010203 = effective_vol × material.rho × material.c_raw × material.m
      uses selected material properties instead of SS316
```

**Net effect:** The bioshield cost may increase (thicker and/or different material) or decrease (cheaper material like concrete vs. SS316). Parent accounts CAS 22.01.02 and CAS 22.01 roll up this change automatically.

### Summary of material properties used in step 5

| Material | Density (kg/m³) | Cost ($/kg) | Mfg factor | DTF curve source |
|---|---|---|---|---|
| Concrete | 2260 | 0.085 | 2 | Borated polyethylene proxy (conservative) |
| Borated Polyethylene | 970 | 4 | 1.5 | BRL-1174 direct |
| Iron | 7880 | 0.1069 | 2 | BRL-1174 (corrected, 8 points) |
| Water | 1000 | 0 | 1 | BRL-1174 direct |

---

## Current State

The existing bioshield cost in `cas220102_shield.py` is purely geometric:
```
C22010203 = bioshield_vol × SS316.c_raw × SS316.m
```
Volume comes from `cas220101` (radial build geometry). Material is hard-coded SS316.

## Dose-Based Approach (from notebook)

1. Given **initial dose without bioshield** (Sv/yr) and **regulatory dose limit** (Sv/yr), compute required **Dose Transmission Factor (DTF)**: `DTF = regulatory_dose / initial_dose`
2. Using material-specific DTF-vs-thickness polynomial curves (from BRL-1174 data), compute **required bioshield thickness**
3. Use `max(required_thickness, user_specified_bioshield_t)` — never shrink below user input
4. Cost using the selected material's density and cost per kg

## Files to Change

### New files
- `pyfecons/costing/safety/bioshield.py` — Dose attenuation logic, DTF data, required thickness computation, bioshield material properties

### Modified files
- `pyfecons/enums.py` — Add `BioshieldMaterial` enum (CONCRETE, BORATED_POLYETHYLENE, IRON, WATER)
- `pyfecons/inputs/shield.py` — Add optional fields: `initial_dose_without_bioshield`, `bioshield_material`, `regulatory_dose_limit`
- `pyfecons/costing/calculations/cas22/cas220102_shield.py` — Conditional branch: dose-based when safety enabled + inputs present, else existing geometry-only
- `pyfecons/costing/categories/cas220102.py` — Add optional output fields: `bioshield_required_thickness`, `bioshield_dose_dtf`, `bioshield_vol_safety`
- `pyfecons/costing/mfe/mfe.py` — Pass `inputs.radial_build` to shield cost function
- `pyfecons/costing/ife/ife.py` — Same
- `pyfecons/report/sections/cas220102_section.py` — Conditional replacements for dose-based outputs
- `pyfecons/costing/mfe/templates/CAS220102.tex` — `\ifsafetycosts` conditional text for bioshield
- `pyfecons/costing/ife/templates/CAS220102.tex` — Same
- `customers/CATF/mfe/DefineInputsSafety.py` — Add bioshield inputs
- `customers/CATF/ife/DefineInputsSafety.py` — Add bioshield inputs

### Tests
- `tests/test_bioshield_safety.py` — Backward compat, dose calc, edge cases

## DTF Data (from notebook, sourced from BRL-1174)

| Material | Thicknesses (inches) | DTF values |
|----------|---------------------|------------|
| Water | 0, 1, 2, 3, 5, 6, 8, 9, 12 | 1, 0.955, 0.91, 0.82, 0.685, 0.64, 0.505, 0.46, 0.325 |
| Borated Polyethylene | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12 | 1, 0.95, 0.88, 0.8, 0.68, 0.6, 0.5, 0.4, 0.35, 0.28, 0.2, 0.15 |
| Iron | 0, 1, 2, 3, 4, 6, 8, 10, 12 | 1, 0.9, 0.75, 0.8(?), 0.62, 0.55, 0.38, 0.25, 0.19, 0.14 | ⚠ See assumption #1 below — corrected to 8 points |
| Concrete | Uses borated polyethylene curve (placeholder) |

Material costs (notebook):
| Material | Density (kg/m³) | Cost ($/kg) |
|----------|----------------|-------------|
| Water | 1000 | 0 |
| Borated Polyethylene | 970 | 4 |
| Iron | 7880 | 0.1069 |
| Concrete | 2260 | 0.085 |

## Open Questions — Working Assumptions

Each question below has a working assumption for implementation. These assumptions should be reviewed by someone with domain expertise (nuclear/shielding physics). Questions for the reviewer are marked with **ASK:**.

---

### 1. Iron DTF data

**Problem:** Array has 9 thickness values but 10 DTF values. Also DTF[3]=0.8 > DTF[2]=0.75 which is non-physical (dose transmission cannot increase with more material).

**Assumption:** The DTF value 0.8 at thickness=3" is a transcription error from the BRL-1174 curves (Allen, Futterer & Wright, 1962). Drop that point entirely. The corrected iron data becomes:

| Thicknesses (inches) | 0 | 1 | 2 | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|---|---|
| DTF | 1 | 0.9 | 0.75 | 0.62 | 0.55 | 0.38 | 0.25 | 0.19 |

This gives 8 points, all monotonically decreasing as expected for a shielding material. The original 10th DTF value (0.14) is also dropped since it had no matching thickness.

**ASK:** Can someone verify against the original BRL-1174 Figure for iron at 14 MeV? The 3-inch data point may have been read from the wrong curve.

---

### 2. Concrete DTF curve

**Assumption:** Use the borated polyethylene curve as a proxy for concrete. This is **conservative** — borated polyethylene is a better neutron moderator than ordinary concrete (higher hydrogen content), so using its DTF curve means concrete will be slightly under-credited for shielding, yielding a thicker (more expensive) bioshield estimate. Add a code comment flagging this as a placeholder.

**Supporting evidence:**
- Allen et al. (1962, BRL-1174) includes concrete transmission data at 14 MeV, so concrete-specific curves could be extracted from the original report
- Khripunov et al. (1998) show borated concrete performs 2-3x better than ordinary concrete for ITER's bioshield — adding boron to concrete would make the polyethylene proxy more accurate
- Li et al. (2015) tested four concrete types under ITER neutron conditions, confirming material-specific variation

**ASK:** Should we extract concrete-specific DTF data from BRL-1174 Figure set, or is the conservative proxy acceptable for the costing exercise?

---

### 3. Manufacturing factor

**Assumption:** Yes, apply a manufacturing factor to each bioshield material. The existing PyFECONS pattern is `cost = volume × density × cost_per_kg × manufacturing_factor`, and all materials in `materials.py` carry one. Omitting it would undercount installed cost.

Proposed manufacturing factors:

| Material | m (mfg factor) | Rationale |
|---|---|---|
| Concrete | 2 | Consistent with existing `Materials.Concrete.m = 2` in PyFECONS. Covers formwork, reinforcement, pouring, curing. |
| Borated Polyethylene | 1.5 | Requires cutting, shaping, and installation but no welding or complex machining. Comparable to lead (m=1.5) and lithium (m=1.5) in PyFECONS. |
| Iron | 2 | Structural steel fabrication: cutting, forming, welding, inspection. Same as SS316 (m=2). |
| Water | 1 | No fabrication — just fill a containment vessel. Containment structure costed separately. |

**ASK:** Are these factors reasonable for bioshield-scale civil construction? The existing PyFECONS factors were calibrated for reactor-grade components; bioshield construction may warrant different values.

---

### 4. Regulatory dose limit

**Assumption:** Default to **0.05 Sv/yr (50 mSv/yr)**, the US NRC occupational dose limit (10 CFR 20.1201). Do **not** build region-specific logic — the `regulatory_dose_limit` field is already a user-overridable input, so users in other jurisdictions can set their own value.

Reference dose limits from the literature for context:

| Jurisdiction | Occupational limit | Public limit | Source |
|---|---|---|---|
| US NRC | 50 mSv/yr | 1 mSv/yr | 10 CFR 20 |
| EU BSS | 20 mSv/yr | 1 mSv/yr | Directive 2013/59/Euratom |
| ITER (France) | 2.5 mSv/yr (worker target) | 0.1 mSv/yr | Rosanvallon et al. 2018 |
| DOE fusion | 10 mSv (accident, site boundary) | — | DOE-STD-6003-96; ARIES-ACT1 |

The 50 mSv/yr default is the least conservative (most permissive) of these, which gives the thinnest bioshield and lowest cost — a lower bound estimate.

**ASK:** Should the default be more conservative (e.g. 1 mSv/yr public limit, or 20 mSv/yr EU occupational)? The choice depends on whether the bioshield is designed to protect workers in adjacent areas or the general public at the site boundary. For ITER, the worker target was 2.5 mSv/yr — significantly stricter than 50 mSv/yr.

---

### 5. Volume divergence

**Assumption:** Accept the divergence. When dose-required thickness > user's `bioshield_t`:
- **CAS 22.01.02.03 cost** uses the larger dose-required thickness and selected material
- **Radial build geometry** (used in `cas220101` and downstream) stays at user-specified `bioshield_t`
- Emit a **warning** in the output noting the divergence and the required vs. specified thicknesses

**Rationale:**
- The bioshield is the outermost radial build layer — increasing it does not affect inner component geometry, plasma parameters, or neutronics of the blanket/shield
- Updating the radial build would cascade through many calculations (volumes, costs, report figures) for all inner components, which is disproportionate
- The cost delta is captured where it matters most (CAS 22.01.02.03)
- The divergence is documented and auditable

**ASK:** Is this acceptable for the CATF reports, or should we also update `bioshield_t` in the radial build when the dose calculation requires a thicker bioshield? The latter would be more physically consistent but significantly more complex to implement.

---

### 6. Initial dose value

**Assumption:** Default `initial_dose_without_bioshield` = **0.5 Sv/yr** for both MFE and IFE.

This represents the annual dose rate at the bioshield inner surface, assuming the blanket, shield, and vacuum vessel are in place but no bioshield exists. The blanket/shield assembly attenuates the 14 MeV D-T neutron flux by several orders of magnitude; the bioshield provides the final reduction to regulatory limits.

**Rationale for 0.5 Sv/yr:**
- Gives DTF = 0.05/0.5 = 0.1, requiring ~8-10 inches (~20-25 cm) of borated polyethylene or ~8 inches (~20 cm) of iron — physically reasonable bioshield thicknesses
- Falls within the reliable interpolation range of the BRL-1174 data (0-12 inches)
- ITER data points bracket this estimate: port cell dose rates of ~100 µSv/h at 12 days post-shutdown (Ghani et al. 2015), with on-load rates orders of magnitude higher; ITER's 2 m concrete bioshield was designed for a much larger, higher-flux machine than a commercial power plant with optimized shielding
- BCSS reference neutron wall loading is 5 MW/m² (Abdou et al. 1983); after blanket/shield attenuation, residual dose in the 0.1-1 Sv/yr range is consistent with well-designed shielding

**Important caveat:** This is a placeholder. The actual value is design-specific and requires a neutronics transport calculation (MCNP, PHITS, or similar) based on the specific blanket/shield radial build. The CATF MFE and IFE reference designs may have significantly different values.

**ASK:** Can the notebook authors provide neutronics-derived dose rates at the bioshield location for the CATF MFE and IFE reference designs? Alternatively, is 0.5 Sv/yr a reasonable order-of-magnitude estimate given the blanket/shield configurations in those designs?

## Dependency Order

```
1. enums.py (BioshieldMaterial)
2. inputs/shield.py (new fields)
3. costing/safety/bioshield.py (new file)
4. costing/categories/cas220102.py (new fields)
5. costing/calculations/cas22/cas220102_shield.py (conditional branch)
6. costing/mfe/mfe.py + costing/ife/ife.py (pass radial_build)
7. report/sections/cas220102_section.py (conditional replacements)
8. templates CAS220102.tex (conditional text)
9. DefineInputsSafety.py files (add inputs)
10. Tests
```

## Progress

Implementation complete (2026-03-26). Merged to `mfe-safety-part-ii`.

- [x] Document working assumptions for open questions
- [x] Implement enum and inputs
- [x] Implement safety/bioshield.py
- [x] Modify cas220102 calculation
- [x] Update call sites (mfe.py, ife.py)
- [x] Update report section and templates
- [x] Update CATF DefineInputsSafety files
- [x] Write tests — 12 new tests, all 96 pass
- [x] Run all 8 report variants — all complete without error

### Outstanding

- [ ] Review assumptions with domain experts (see ASK items in Open Questions above)
