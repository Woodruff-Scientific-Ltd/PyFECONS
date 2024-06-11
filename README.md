# PyCosting
PyFECONs is a general fusion costing analysis tool derived from 
[ARPAE-PyFECONS](https://github.com/Woodruff-Scientific-Ltd/ARPAE-PyFECONS) scripts. The library has two purposes:

(1) Perform costing calculations for MFE, IFE, and MIF reactor concepts

(2) Generate a comprehensive report with the cost analysis.


## Running the costing code

Follow the steps below for [Installing Dependencies](#installing-dependencies) with conda or pyvenv + pip.

Create a new customer folder in the customers/ directory. CATF is the example customer.

Create a subdirectory in the customer folder for each reactor type ife/, mfe, or mif/, you'll see examples in CATF/.

Copy and paste the DefineInputs.py for the given reactor type and update the parameters to your specification.

Then you can run the script in the top level PyFECONs directory:
```bash
python3 RunCostingForCustomer.py REACTOR_TYPE CUSTOMER_FOLDER
```

An example run for CATF mfe:
```bash
python3 RunCostingForCustomer.py mfe CATF
```

This will use inputs from `customers/CATF/mfe/DefineInputs.py` file, output assets to `customers/CATF/mfe/outputs/`,
and create a copy of the inputs `input.json` and outputs `data.json`.

### Customer Custom Templates

You can override the library templates in `pyfecons/costing/REACTOR_TYPE/templates` folder by adding a template of the
exact same file name to the `customers/CUSTOMER_NAME/REACTOR_TYPE/templates` directory. The costing code will use
files in the `customers/` directory before the library with the same substitutions.

### Customer Custom Included Files

You can override the library included files in `pyfecons/costing/REACTOR_TYPE/included_files` folder by adding a
template of the exact same file name to the `customers/CUSTOMER_NAME/REACTOR_TYPE/included_files` directory.
The costing code will use  files in the `customers/` directory before the library with the same substitutions. NB you
must have the file in the same directory structure relative to `included_files/`.
I.e. `customers/CATF/ife/included_files/StandardFigures/WSLTD_logo.png`.

## Importing PyFECONs into your project

### Pip

To import pyfecons version `X.Y.Z` into your pip project:

```
pip install pyfecons @ git+ssh://git@github.com/Woodruff-Scientific-Ltd/PyFECONS.git@X.Y.Z
```

### Conda

To import pyfecons version `X.Y.Z` into your conda project, add the following to `environment.yml`:
```
...
- pip:
  - --upgrade git+https://github.com/Woodruff-Scientific-Ltd/PyFECONS.git@X.Y.Z
```

## Contributing to this Library

### Managing dependencies

Please add new dependencies to the `environment.yml` -pip array and duplicate these to `requirements.txt` file.

### Making changes

Please use [git branches](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) and create pull requests for approval when making changes.

### Updating the library version

We need to update the library version number in `setup.py` when making changes. We are using `MAJOR.MINOR.PATCH` version number system.
* `MAJOR` - increment when significant structure of the library has changed or new feature is introduced.
* `MINOR` - increment when library has changed enough that UI changes are required (i.e. introduce new inputs or outputs).
* `PATCH` - increment when changes are pushed, but UI would not need to be updated (i.e. changes to calculations, templates, but not to inputs or outputs)

### Creating a Github release

After code is updated and merged to main, if the version has changed you'll need to create a new release.
Please follow the [Github Instructions](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
to create a release matching the merged version number. This is important for the webapp to manage updates and changes.

### Creating a key pair
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/your_file.pub
```
Add to GitHub keys.


## Installing Dependencies

The library should work out of the box on linux with a python virtual environment and pip.

Because of OS specific dependencies, in order to use PyFECONs on Mac M1 (and Windows?) you'll need to use conda dependency management in your project. See the steps below in the README for setting this up in your environment.

### Installing LaTeX

LaTeX is an external dependency to the library since installation varies widely by OS.

Mac:
```bash
brew install --cask mactex
```

Linux:
```
sudo apt install texlive-latex-extra
```

Windows
```
TODO
```


### Python Virtual Environment

Preferred dependency management for Linux and Windows.

Linux Commands
```bash
# remove existing environment (on clean up)
rm -rf venv

# create virtual environment (on new environment)
python3 -m venv venv

# activate virtual environment (on new terminal)
source venv/bin/activate

# install dependencies (on new environment or after changes)
pip install -r requirements.txt
```

Windows Commands
```bash
# remove existing environment (on clean up)
rm -rf venv

# create virtual environment (on new environment)
python3 -m venv venv

# activate virtual environment (on new shell)
venv\Scripts\activate

# install dependencies (on new environment or after changes)
pip install -r requirements.txt
```

### Conda Virtual Environment

[Conda](https://docs.conda.io/en/latest/) package management is needed for local development on Mac M1 due to 
incompatibility of [cadquery](https://github.com/CadQuery/cadquery and pip.

Follow the Miniconda [Quick command line install](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
instructions.

Don't forget to init your shell with:

```bash
# Mac zshell
~/miniconda3/bin/conda init zsh

# Or bash
~/miniconda3/bin/conda init bash
```

Conda Commands
```
# create environment - only need to do this once or every time after deleting the environment 
conda env create -f environment.yml

# list environments
conda env list

# activate pyfecons environment
conda activate pyfecons

# updating conda environment (after adidng or removing dependencies)
conda env update -f environment.yml

# deactivating the Conda environment
conda deactivate

# delete environment - to reinstall fresh 
conda env remove -n pyfecons

```
