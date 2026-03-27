# PyFECONS Development

## Testing

After significant changes, run all 8 report combinations (MFE/IFE x lite/full x safety/no-safety) to verify nothing is broken:

```bash
./run_all_costing.sh CATF --mfe
./run_all_costing.sh CATF --ife
```

Each runs 4 combinations (full/lite x safety/no-safety) end-to-end including PDF generation. All 8 must complete without error.

Unit and integration tests are also available via pytest in `tests/`.

Run `./format.sh` before committing to apply Black, isort, and flake8.

## Verification before committing

After running all 8 combinations, review the diffs in these tracked output files under `customers/CATF/`:

- `**/inputs*.json` — costing inputs
- `**/data*.json` — costing outputs
- `**/sections*.json` — template substitution values

Check that:
1. Fields we changed updated as expected
2. Nothing changed that we didn't expect to change
3. No significant changes are missing

These files are the source of truth for what the code produces. Review their diffs before committing and merging.

Before merging a branch, bump the version in `setup.py`.

## Inputs

When adding new input fields, always add corresponding defaults in the CATF customer config files:
- `customers/CATF/mfe/DefineInputs.py`
- `customers/CATF/ife/DefineInputs.py`
- `customers/CATF/mfe/DefineInputsSafety.py` (if safety-related)
- `customers/CATF/ife/DefineInputsSafety.py` (if safety-related)

## Serialization

Safety-only fields must not appear as nulls in non-safety JSON output. Strip them in `toDict()` overrides (`CostingData` for data.json, `AllInputs` for inputs.json).

## Code style

- Keep PDF generation code separate from cost calculations. Costing logic lives in `costing/calculations/`; report/PDF logic lives in `report/` and templates.
- Use substitution variables in all `.tex` template vars — never hard-code computed values in templates.
- New template substitution variables use PascalCase (e.g. `BioshieldMaterial`, `BioshieldDtf`). Legacy variables (e.g. `C22010203`, `VOL9`) keep their existing names.
- Each template substitution variable must be unique within the template file. For numeric cost codes, use the full zero-padded account number (e.g. `C22010203` not `C203`).
- Add paper references whenever possible to `.tex` templates to support traceability of assumptions and data sources.
- See `STYLING.md` for Python formatting rules (Black, isort, flake8, pre-commit hooks).
