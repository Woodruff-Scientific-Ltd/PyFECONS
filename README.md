# PyFECONs - Python Fusion ECONomicS
PyFECONs is a general fusion costing analysis tool derived from 
[ARPAE-PyFECONS](https://github.com/Woodruff-Scientific-Ltd/ARPAE-PyFECONS) scripts. The library has two purposes:

(1) Perform costing calculations for MFE, IFE, and MIF reactor concepts

(2) Generate a comprehensive report with the cost analysis.

See the [pyfecons](pyfecons/README.md) for an overview of the costing code.

See the [deployment](deployment/README.md) section for the electricity cost analysis.

## Running the costing code

Follow the steps below for [Installing Dependencies](#installing-dependencies) with pyvenv + pip.

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

To import PyFECONs version `X.Y.Z` into your pip project:

```
pip install pyfecons @ git+ssh://git@github.com/Woodruff-Scientific-Ltd/PyFECONS.git@X.Y.Z
```

### Conda

To import PyFECONs version `X.Y.Z` into your conda project, add the following to `environment.yml`:
```
...
- pip:
  - pyfecons @ git+ssh://git@github.com/Woodruff-Scientific-Ltd/PyFECONS.git@X.Y.Z
```

## Contributing to this Library

### Managing dependencies

Please add new dependencies to the `requirements.txt` file.

### Making changes

Please use [git branches](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) and create pull requests for approval when making changes.

### Style and standards

We use [Black](https://black.readthedocs.io/en/stable/) for Python formatting. To help your code adhere, you can: install the Black linter or formatter in your IDE of choice; [use](https://black.readthedocs.io/en/stable/integrations/source_version_control.html) local [pre-commit](https://pre-commit.com/) hooks; or rely on our Github actions workflow to give you hints.  

```bash
# run style check without fixing file
black --check .

# run style check and fix files
black .

```

### Updating the library version

We need to update the library version number in `setup.py` when making changes. We are using `MAJOR.MINOR.PATCH` version number system.
* `MAJOR` - increment when significant structure of the library has changed or new feature is introduced.
* `MINOR` - increment when library has changed enough that UI changes are required (i.e. introduce new inputs or outputs).
* `PATCH` - increment when changes are pushed, but UI would not need to be updated (i.e. changes to calculations, templates, but not to inputs or outputs)

### Creating a Github release

After code is updated and merged to main, if the version has changed you'll need to create a new release.
Please follow the [Github Instructions](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
to create a release matching the merged version number. This is important for the webapp to manage updates and changes.

## Installing Dependencies

The library should work out of the box on linux with a python virtual environment and pip.

### Installing LaTeX

If you want to generate reports, you will need to install some packages for LaTeX - which is an external dependency to the library since installation varies by OS.

Mac:
```bash
brew install --cask mactex
```

Linux:
```
sudo apt install texlive-latex-extra
sudo apt-get install texlive-font-utils
```

Windows
The most common way to install LaTeX on Windows is by using MiKTeX. Here's a step-by-step guide:
(1) Download MiKTeX from the [MiKTeX website](https://miktex.org/download)
(2) Run the downloaded installer and follow on-screen instructions
(3) Once installation is complete, open the MiKTeX Console from the start menu, and check for updates to make sue you have the latest one
(4) Install a LaTeX editor to write your LaTeX documents. TeXstudio and TeXworks are a couple of options. This is optional
(5) Create a simple LaTeX document to test the installation, e.g. test.tex. Open the test.tex file in TeXstudio/TeXworks and compile it. If using the command line, navigate to the directory where test.tex is saved and run:
```
pdflatex test.tex
```

### Installing Python 3.10

Library is tested working with Python 3.10 (3.10.14).

We recommend [pyenv](https://github.com/pyenv/pyenv) for Python version management on MacOS / Linux and [pyenv-win](https://github.com/pyenv-win/pyenv-win) for Windows.

Please follow the installation instructions for [MacOS/Linux pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) or [Windows pyenv-win](https://github.com/pyenv-win/pyenv-win?tab=readme-ov-file#quick-start).

Example commands for MacOS:
```
# install pyenv
brew install pyenv

# set up shell
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# install python version
pyenv install 3.10

# optional, set it as global version
pyenv global 3.10

# verify python version
python3 --version
```

### Python Virtual Environment

We use [Python venv](https://docs.python.org/3/library/venv.html) for dependency management. Make sure the correct
python version is enabled when the virtual environment is created (test with `python3 --version`).

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

## Tests

Testing is done with [pytest](https://docs.pytest.org/en/stable/). To run them, navigate to this directory and run:

```
pytest tests/
``` 
