# PyCosting
It's PyFecons, but with a different name.

# Using this library

## Dependency Management

The library should work out of the box on linux python virtual environment. 

Because of OS specific dependencies, in order to use PyFECONs on Mac M1 (and Windows?) you'll need to use conda dependency management in your project. See the steps below in the README for setting this up in your environment.

If your system requires conda, then you will need to copy and paste the [environment.yml](https://github.com/nTtau/PyFECONS/blob/main/environment.yml) file to your project and add your project's dependencies.

## Pip

To import pyfecons version `X.Y.Z` into your pip project:

```
pip install pyfecons @ git+ssh://git@github.com/nTtau/PyFECONS.git@X.Y.Z
```

## Conda

To import pyfecons version `X.Y.Z` into your conda project, add the following to `environment.yml`:
```
- pip:
  - --upgrade git+https://github.com/nTtau/PyFECONS.git@X.Y.Z
```

Unfortunately, due to the OS specific dependencies of [cadquery](https://github.com/CadQuery/cadquery), it's impossible to support an independent library that works pip virtual environments.

## Making changes

Please use [git branches](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) and create pull requests for approval when making changes.

## Updating the library version

We need to update the library version number in `setup.py` when making changes. We are using `MAJOR.MINOR.PATCH` version number system.
* `MAJOR` - increment when significant structure of the library has changed or new feature is introduced.
* `MINOR` - increment when library has changed enough that UI changes are required (i.e. introduce new inputs or outputs).
* `PATCH` - increment when changes are pushed, but UI would not need to be updated (i.e. changes to calculations, templates, but not to inputs or outputs)

## Creating a Github release

After code is updated and merged to main, if the version has changed you'll need to create a new release.
Please follow the [Github Instructions](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
to create a release matching the merged version number. This is important for the webapp to manage updates and changes.

## Installing LaTeX
We are using native LaTeX to compile the pdf. You'll need to have `pdflatex` and `bibtex` installed and working on your system. Here's an unverified [guide](https://github.com/James-Yu/LaTeX-Workshop/wiki/Install) recommending TexLive.

### Mac

Simply use `brew install mactex`.

### Linux

```
sudo apt-get update
sudo apt-get install texlive texlive-font-utils
```

### Windows

TODO

## Creating a key pair
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/your_file.pub
```
Add to GitHub keys.

# Installing dependencies

Most dependency management is done with python virtual environment and pip. LaTeX will need to be installed outside the environment. cadquery works on linux with pip, but requires conda to work on Mac M1. `requirements.txt` is the main dependency file, but replicated to `environment.yml` to be used by conda for M1.

TODO verify dependencies on Windows. For now consider using conda.

## Python Virtual Environment

Linux and deployment server.

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

## Conda Virtual Environment

[Conda](https://docs.conda.io/en/latest/) package management is needed for local development on Mac M1 due to 
incompatibility of [cadquery](https://github.com/CadQuery/cadquery and pip.

### Conda Installation

Follow the Miniconda [Quick command line install](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
instructions.

Don't forget to init your shell with:

```bash
# Mac zshell
~/miniconda3/bin/conda init zsh

# Or bash
~/miniconda3/bin/conda init bash
```

### Creating the Conda environment

You'll only need to do this once or every time after deleting the environment.

```bash
conda env create -f environment.yml
```

### Listing Conda environments

```bash
conda env list
```

You should see the `pyfecons` environment when created successfully.

### Activating the Conda environment

You'll need to do this fer every new shell.

```bash
conda activate pyfecons
```

If this throws an error saying activate command is missing, you have a problem with your conda installation or didn't
run the init command.


### Updating the Conda environment

You'll need to do this when you add or remove a package from the environment.yml file:

```bash
conda env update -f environment.yml
```

### Deactivating the Conda environment

You'll need to do this only to detach from the Conda environment in the current shell:

```bash
conda deactivate
```

### Deleting the Conda environment

You'll need to do this only if you want to reinstall your environment to ensure a working environment.yml file.

```bash
conda env remove -n pyfecons
```

### Managing dependencies

Please add new dependencies to the `environment.yml` -pip array and duplicate these to `requirements.txt` file.

## Installing LaTeX

LaTeX is an external dependency to the library since installation varies widely by OS.

### Mac

```bash
brew install --cask mactex
```

### Linux

```
sudo apt install texlive-latex-extra
```

### Windows

TODO

## Running the costing code

With an environment set up correctly, run the following command to execute the costing code:

```bash
python3 RunCostingForCustomer.py "CATF"
```

Which, working from the `customers/CATF/` folder, will take inputs from the `DefineInputs.py` file and
output `inputs.json`, `data.json`, and `output/` processed template files.
