# PyFECONs Costing

## inputs.py - Main Inputs Class

The `Inputs` is the main input class. See [mfe/DefineInputs.py](../customers/CATF/mfe/DefineInputs.py) for an example
usage.

## pyfecons.py - Main Runner Class

This class contains the main entry functions for creating a report. The usage is as follows:

```
inputs = AllInputs(...)
costing_data = RunCosting(inputs)
report_content = CreateReportContent(inputs, costing_data)
report = RenderFinalReport(report_content, hide_output=True)
```

## data.py - Main Output Class

This contains the `Data` class, the main output data, the result of costing calculations ran in `RunCosting`.

## Costing Code

The main costing code lies in `costing` package. `calculations` contains shared code and classes while each reactor type
contains it's costing code in `ife`, `mfe`, and `mif` package respectively.

For each reactor type package (i.e. `ife/`), the `templates/` folder contains the LaTeX template files that are used 
in template hydration. The `included_files/` folder contains files to be included in the LaTeX compilation in the same
relevant path as this folder. And the rest of the code are costing categories starting with CASXXX.

The main entry point to the costing code is in the `ife.py`, `mfe.py`, and `ife.py` files. Each of these fulfills a
`GenerateCostingData` function that takes the inputs and runs all the costing code.

The main machinery here is as follows:

```
def GenerateCostingData(inputs: AllInputs) -> CostingData
    data = Data(reactor_type=ReactorType.IFE)
    template_providers = [
        power_balance(inputs, data),
        cas_10(inputs, data),
        ...
    ]
    return CostingData(data, template_providers) 
```

Here initialization of `template_providers` runs each costing category in succession, updates the results data, and
returns the "fulfilled" templates.

`costing_data.py` contains `ReportSection` class, which is the main data of a costing calculation.

```
class ReportSection:
    # template substitutions variable_name -> value
    replacements: dict[str, str] = field(default_factory=dict)
    # template file name in templates/ directory
    template_file: str = None
    # latex path -> image bytes
    figures: dict[str, bytes] = field(default_factory=dict)
    # template file path for LaTeX compilation directory (defaults to Modified/{template_file})
    _tex_path: str = None
```

Each costing category CASXX takes inputs and output data, then returns a subclass of `ReportSection` representing 
the computed cost category. For example, for cost category CAS10:

This is the example output class:
```
class CAS10(ReportSection):
    C100000: M_USD = None
    ...
```

And an outline of the costing calculation:
```
def cas_10(inputs: AllInputs, data: Data) -> ReportSection
    OUT = data.cas10  # grabs the initialized ReportSection from data class
    ... do calculations ...
    OUT.C100000 = M_USD(...)
    OUT.template_file = 'CAS100000.tex'
    OUT.replacements = {
        'C100000': round(OUT.C100000),
        ...
    }
    OUT # returns processed ReportSection
```

Every cost category will follow this pattern.

Finally, the `PyCosting_ARPA_E_XXX2.ipynb` and `pycosting_arpa_e_xxx2.py` files represent versions of the ARPAE 
collab costing code ported over. To syncronize changes, the idea is to save each of these files here and add
the changes to the costing library.

