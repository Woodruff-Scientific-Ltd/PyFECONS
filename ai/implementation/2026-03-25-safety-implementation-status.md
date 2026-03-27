# Safety Implementation Status — PyFECONS

Cross-reference of the Safety Implementation document (`ai/docs/safety/2025-03-25 - Safety implementation.pdf`) against the current PyFECONS codebase. Includes findings from the hazard mapping CSVs and the CATF_Ongoing_Changes notebook.

## Source Documents

- `ai/docs/safety/2025-03-25 - Safety implementation.pdf` — Implementation plan (7 hazards in table form)
- `ai/docs/safety/2025-03-25 - Mapping hazards - MFE.csv` — Full MFE hazard-to-cost-category mapping
- `ai/docs/safety/2025-03-25 - Mapping hazards - IFE.csv` — IFE hazard mapping (structure only, no hazard details filled in)
- `ai/docs/safety/2025-03-25 - Mapping hazards - MIF.csv` — MIF hazard mapping (structure only)
- `ai/docs/safety/2025-03-25-CATF_Ongoing_Changes.ipynb` — Research notebook with calculations for oxidation, bioshield, tritium, licensing, insurance, etc.
- `ai/docs/safety/2025-03-25-catf_ongoing_changes.py` — Python export of the notebook

## Implementation Summary

| # | Hazard | Cost Category | Fusion Type | Plan Status | Code Status | Notes |
|---|--------|---------------|-------------|-------------|-------------|-------|
| 1 | Plasma Disruption Effects | CAS 22.01.20 (new) | MFE only | EASY | **DONE** | Fixed cost with inflation from ITER basis |
| 2 | Rapid Structural Oxidation | CAS 22.01.01 First Wall | MFE only | MEDIUM | **NOT IMPLEMENTED** | Notebook has full calculation; not in library |
| 3 | Bioshield | CAS 22.01.02.03 | MFE and IFE | MEDIUM | **PARTIALLY DONE** | Material cost exists; safety-specific dose-based sizing not implemented |
| 4 | Radioactive Release of Tritium | CAS 11 Land & Land Rights | MFE and IFE | Required before webinar | **DONE** | Polynomial fit from Lukacs & Williams (2020) |
| 5 | Hot Cell Radioactivity | CAS 22.06.06 (new) | MFE only | EASY | **DONE** | Fixed $55M from ITER contract |
| 6 | Licensing | CAS 13 Plant Licensing | MFE and IFE | EASY | **DONE** | Region-based (US/UK) fixed add-ons |
| 7 | Insurance | New Category (CAS 78) | MFE and IFE | EASY | **DONE** | LSA-scaled from fission baseline |

**5 of 7 hazards fully implemented. 1 not implemented. 1 partially done.**

---

## Detailed Status per Hazard

### 1. Plasma Disruption Effects — DONE

**Plan:** New CAS 22.01.20 Disruption Mitigation System. Fixed cost. MFE only. "EASY"

**Implementation:**
- `pyfecons/costing/safety/disruption_mitigation.py` — Calculates cost from ITER base (5,664,330 USD in 1989 dollars) inflated to present year
- `pyfecons/costing/categories/cas220120.py` — Category class
- `pyfecons/costing/mfe/templates/CAS220120.tex` — Report template
- Activated by `include_safety_hazards_costs = True`, MFE only
- Git: commit `c2f6b18`
- **Output:** $13.2M (CATF MFE safety run)

### 2. Rapid Structural Oxidation / First Wall Coating — NOT IMPLEMENTED

**Plan:** Under CAS 22.01.01 First Wall. Inputs: oxidation temperature, operating temperature. Output: cost of first wall coating. MFE only. "MEDIUM — we already started implementing this one year ago adding details to the materials library"

**What exists:**
- The CATF_Ongoing_Changes notebook (`ai/docs/safety/`) has the full calculation:
  - Relative Consequence Index (RCI) formula: `RCI = (T_lt(HT-9) - T_o(HT-9)) / (T_lt - T_o)`
  - If RCI < 1: calculate tungsten first wall coating cost
  - Cost components: material cost (tungsten, 600 m² surface, 1mm thickness), application cost (plasma spray at $50/m²), R&D cost (50% of material)
  - Total coating cost calculated in notebook
  - Oxidation temperatures for 316 SS (1010°C), HT-9 (1400°C), Vanadium (700°C), TZM (700°C)
- The materials library in PyFECONS has material properties that could support this
- The safety appendix templates mention oxidation but have no calculated values

**What's missing:**
- No calculation code in `pyfecons/costing/` for first wall coating costs
- No input parameters for oxidation temperature in the input classes
- No integration into CAS 22.01.01 costing
- No template placeholders for coating cost in CAS220101 templates

**To implement:** Port the notebook calculation into a new safety costing module. Add oxidation temperature inputs. Integrate into CAS 22.01.01 section or create a sub-category.

### 3. Bioshield — PARTIALLY DONE

**Plan:** Already calculated in CAS 22.01.02 (Blanket/Shield). Inputs: initial dose without bioshield, material of bioshield. Output: cost for bioshield. MFE and IFE. "MEDIUM — substitution of calculation and explanation in report"

**What exists:**
- `pyfecons/costing/calculations/cas22/cas220102_shield.py` — Bioshield material cost (CAS 22.01.02.03) calculated from volume × material density × cost
- Uses SS316 material properties
- Volume derived from radial build geometry (`bioshield_t` input parameter)
- Template includes bioshield cost line (C22010203) and penetration shielding (C22010204)

**What's missing:**
- No dose-based calculation — the bioshield cost is purely geometric/material, not driven by safety requirements (dose levels, shielding effectiveness)
- No input for "initial dose without bioshield" as the plan specifies
- No safety-specific substitution of the bioshield calculation or explanation as the plan describes
- The plan says "medium substitution of calculation and explanation in report" — the report text and calculation methodology should be updated to reflect safety-driven sizing

**To implement:** Add dose-based bioshield sizing (inputs: dose rate, target dose limit, shielding material attenuation). Replace or augment the geometric-only calculation with one that validates the bioshield thickness against radiation safety requirements.

### 4. Radioactive Release of Tritium — DONE

**Plan:** Land costs in CAS 11. Inputs: HTO inventory (g), dust tritium inventory (g/month), stack height. Output: cost of site. MFE and IFE. "Required before webinar"

**Implementation:**
- `pyfecons/costing/calculations/cas10_pre_construction.py` — Calculates C110200 (safety land add-on) using polynomial fit from Lukacs & Williams (2020)
- `pyfecons/inputs/tritium_release.py` — TritiumRelease dataclass with `hto_inventory_g`, `dust_tritium_inventory_g_per_month`, `stack_height_m`
- Distance-to-site-boundary calculated from dust tritium, then `area = π × distance²`, costed at $3,800/acre (USDA 2022)
- Currently US region only (UK would need different land values)
- Git: commit `f279509`
- **Output:** C110200 = $3.6M (CATF safety runs)

**Note from plan:** "I think the costs can be substituted with the safety calculation entirely (added as a 2026 update?)" — suggests the safety-driven land cost could eventually replace the baseline land cost entirely, not just be an add-on.

### 5. Hot Cell Radioactivity / Remote Handling — DONE

**Plan:** New CAS 22.06.06 Remote Handling Equipment. Fixed cost. MFE only. "EASY"

**Implementation:**
- `pyfecons/costing/safety/remote_handling.py` — Fixed $55M based on ITER divertor remote handling contract
- `pyfecons/costing/categories/cas220606.py` — Category class
- `pyfecons/costing/mfe/templates/CAS220606.tex` — Report template referencing MASCOT/JET and ITER
- Git: commit `904427e`
- **Output:** $55.0M (CATF MFE safety run)

### 6. Licensing — DONE

**Plan:** CAS 13 Plant Licensing. Input: country (UK or US). Output: cost of license. MFE and IFE. "EASY"

**Implementation:**
- `pyfecons/costing/safety/licensing.py` — Region-based add-ons to baseline $210M licensing cost
  - US: +$53.5M (NRC byproduct materials licensing midpoint)
  - UK: +$0.070M (REPPIR 2019 + Environment Agency fees)
  - Other regions: +$0
- Git: commit `4f99b16`
- **Output:** C130000 = $263.5M for US (baseline $210M + $53.5M safety add-on)

### 7. Insurance — DONE

**Plan:** Entirely new cost category. Input: operating years. Output: cost of insuring the plant. MFE and IFE. "EASY"

**Implementation:**
- `pyfecons/costing/safety/insurance.py` — Annual premium based on US fission baseline ($1.1M/yr) scaled by LSA level
  - LSA 1: 19% → $209K/yr
  - LSA 2: 19% → $209K/yr
  - LSA 3: 23% → $253K/yr
  - LSA 4: 23% → $253K/yr
- Added to CAS 70 (O&M) and reported in CAS 78
- Git: commit `7559f19`
- **Output:** $0.209M/yr (CATF, LSA 2)

**Note:** The plan mentions "operating years (could be fixed to 40)" as an input, but the current implementation only computes annual cost, not lifetime total. The annual cost is already folded into the LCOE calculation through CAS 70.

---

## Broader Hazard Mapping (from CSVs) — Items Not in Implementation Plan

The MFE hazard mapping CSV (`2025-03-25 - Mapping hazards - MFE.csv`) identifies many more hazard-to-cost-category relationships beyond the 7 in the implementation plan. These are documented as context but most represent "safety by design" considerations rather than new cost categories:

### Hazards referenced but not separately costed:
- **LOCA/LOFA/LOHR** (CAS 21.4 Cooling Structures) — Emergency core cooling, pressure suppression. Cost referenced to CAS 21.4 but no specific safety add-on implemented.
- **Quench of magnetic coils** (CAS 22.1.3) — Quench detection/protection systems. Noted as "hazard not present" in HCI (coils fail safely). No safety cost add-on.
- **Cybersecurity** (CAS 22.7 I&C) — Noted as hazard but no cost implementation.
- **External hazards** (aircraft impact, seismic) — Discussed extensively in notebook. Currently handled via `StructurePga` input (seismic design level) in CAS 22.01.05 Primary Structure. No aircraft impact cost.
- **Vacuum vessel pressure suppression** (CAS 21.4) — VVPSS discussed in notebook for hydrogen/dust explosion mitigation. No separate costing.
- **Cryogenic hazards** (CAS 21.16) — Safety by design, no cost add-on.

### IFE and MIF hazard mappings:
- IFE CSV has structure only — no hazard details filled in yet
- MIF CSV has structure only — no hazard details filled in yet
- Both need the same treatment as MFE to identify applicable hazards and mitigations

---

## Notebook Calculations Not Yet in Library

The CATF_Ongoing_Changes notebook contains several calculations that are researched but not ported to PyFECONS:

1. **First wall coating cost** (oxidation mitigation) — Full calculation with RCI, material costs, application costs
2. **Safety margin for damage/melting** — SM_d and SM_m formulas for first wall under disruption
3. **Mass transport RCI** — Corrosion rate based consequence index
4. **Radioactivity release RCI** — Releasable inventory based consequence index
5. **Cryogenics cost** — Reference to ITER cryogenics ($65M), not integrated as safety-specific
6. **Detailed materials database** — Extensive material properties (oxidation temps, costs, densities) partially overlapping with PyFECONS materials library

---

## Git History (Safety Implementation Commits)

All safety work was implemented in the `safety-analysis` branch (PR #106), with follow-up fixes in PRs #107 and #108:

```
c2f6b18 Add support for safety incorporated calculations. Add MFE CAS220120.
7426777 Add fusion_machine_type prefix to report name.
c0f5caf Rename reactor_type to fusion_machine_type.
904427e Add CAS220606 Hot cell radioactivity to mfe safety costing report
ed37d9b Add runner for costing to easily run all report types.
4f99b16 Add region parameter. Add licencing costs for US & UK. Add IFE safety support.
aa457fd Fix tests
7559f19 Add CAS780000 Insurance costing category when safety enabled
f279509 Add tritium release to CAS100000. Create safety inputs. Add tritium release inputs.
45c17e6 Add safety considerations to lite reports.
d4df190 Add safety and hazards appendix to full reports
a296744 Update run all script for --lite --full --safety combinations.
6508466 Fix MFE CAS structure library substitution
5f03d22 Add missing substitutions for safety calculations
b3c3fe1 Reformat Cost Accounting Table keys
```

## Files Read

- `ai/docs/safety/2025-03-25 - Safety implementation.pdf` (via pdftotext)
- `ai/docs/safety/2025-03-25 - Mapping hazards - MFE.csv`
- `ai/docs/safety/2025-03-25 - Mapping hazards - IFE.csv`
- `ai/docs/safety/2025-03-25 - Mapping hazards - MIF.csv`
- `ai/docs/safety/2025-03-25-CATF_Ongoing_Changes.ipynb` (markdown + code cells via jq)
- `PyFECONS/temp/safety-analysis/Safety implementation.txt` (older copy, same content as PDF)
- `pyfecons/costing/safety/disruption_mitigation.py`
- `pyfecons/costing/safety/remote_handling.py`
- `pyfecons/costing/safety/insurance.py`
- `pyfecons/costing/safety/licensing.py`
- `pyfecons/costing/calculations/cas10_pre_construction.py`
- `pyfecons/costing/calculations/cas22/cas220102_shield.py`
- `pyfecons/inputs/tritium_release.py`
- `pyfecons/costing/mfe/templates/CAS220120.tex`
- `pyfecons/costing/mfe/templates/CAS220606.tex`
- `pyfecons/costing/mfe/templates/CAS220102.tex`
- `pyfecons/costing/mfe/included_files/safety_appendix.tex`
- Git log for safety-related commits
