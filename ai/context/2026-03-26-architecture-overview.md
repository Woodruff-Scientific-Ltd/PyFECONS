# PyFECONS Architecture Overview

## Overview

PyFECONS is a fusion power plant costing library. It takes a set of inputs (reactor geometry, materials, financial parameters) and produces costed accounts following the fusion costing standard, plus LaTeX/PDF reports.

## Pipeline

```
DefineInputs.py → AllInputs → RunCosting → CostingData → Report (JSON + LaTeX/PDF)
```

1. **Inputs** (`pyfecons/inputs/`) — Dataclasses for each input group (radial build, shield, blanket, etc.). Collected in `AllInputs`.
2. **Calculations** (`pyfecons/costing/calculations/`) — Pure cost functions. Each takes inputs + upstream outputs, returns a category dataclass. No PDF/report logic here.
3. **Safety** (`pyfecons/costing/safety/`) — Safety-specific cost modules (bioshield, disruption mitigation, remote handling, insurance, licensing). Gated on `basic.include_safety_hazards_costs` flag internally — call sites are unconditional.
4. **Categories** (`pyfecons/costing/categories/`) — Output dataclasses, one per cost account (CAS 22.01.02, etc.).
5. **Orchestration** (`pyfecons/costing/mfe/mfe.py`, `ife/ife.py`) — `GenerateCostingData()` calls calculations in dependency order, wires outputs to inputs.
6. **Report** (`pyfecons/report/sections/`) — Maps category outputs to template substitution dicts.
7. **Templates** (`pyfecons/costing/mfe/templates/`, `ife/templates/`) — LaTeX files with substitution variables. Safety-conditional text uses `\ifsafetycosts...\fi`.

## Key patterns

### Cost function signature
```python
def cas_XXXXXX_costs(basic: Basic, ..., upstream: CASUpstream) -> CASOutput:
    result = CASOutput()
    # compute
    return result
```

### Safety gating
Safety logic lives inside each calculation function, not at the call site:
```python
if not basic.include_safety_hazards_costs:
    result.cost = M_USD(0.0)
    return result
```

### Materials
`Materials` class in `pyfecons/materials.py` holds material properties. Cost formula: `volume * density * cost_per_kg * manufacturing_factor`.

### Serialization
- `SerializableToJSON` base class with `toDict()` / `_attributesToDict()`.
- `CostingData.toDict()` and `AllInputs.toDict()` override to strip safety-only null fields from non-safety JSON output.
- Enums serialize to their value (or `{value, display_name}` if `display_name` exists).

### Template substitutions
- Legacy variables: uppercase/numeric (e.g. `C22010203`, `VOL9`).
- New variables: PascalCase (e.g. `BioshieldMaterial`, `BioshieldDtf`).
- Each variable must be unique within its template file.

## Reactor types

- **MFE** (Magnetic Fusion Energy) — tokamak and mirror configurations. Ring/torus geometry.
- **IFE** (Inertial Fusion Energy) — laser-driven. Spherical geometry.

Both share common calculations (`pyfecons/costing/calculations/`) but have reactor-specific modules under `pyfecons/costing/mfe/` and `pyfecons/costing/ife/`.

## Output variants

8 combinations per customer: MFE/IFE x full/lite x safety/no-safety. Outputs under `customers/{name}/{mfe|ife}/`:
- `inputs.json` / `inputs_safety.json`
- `data.json` / `data_safety.json`
- `sections.json` / `sections_safety.json` (and lite variants)
- `output/` directories with PDFs
