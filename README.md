# PyCosting
It's PyFecons, but with a different name.

# Using this library

## Conda Dependency Management

Because of OS specific dependencies, in order to use PyFECONs you'll need to use conda dependency management in your project. See the steps below in the README for setting this up in your environment.

Then you will need to add all the dependencies in the [environment.yml](https://github.com/nTtau/PyFECONS/blob/main/environment.yml) to your project.

Finally, you can import a version of the library by adding to the environment.yml file in your project:
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

## Installing LaTex
https://github.com/James-Yu/LaTeX-Workshop/wiki/Install

## Creating a key pair
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/your_file.pub
```
Add to GitHub keys.


## Using a Conda virtual environment

We need to use [Conda](https://docs.conda.io/en/latest/) package management to handle OS specific libraries,
mainly [cadquery](https://github.com/CadQuery/cadquery).

### Removing legacy venv

If you were previously using venv, please remove it running `rm -rf venv` to ensure a clean environment.

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

Since Conda specializes in handling machine specific dependencies, we cannot commit the raw dependency file since it
will contain OS specific libraries. You must add the specific package and version to the `environment.yml` file. 
You should prioritize Conda dependencies, only adding to the `pip:` list if the dependency is not in Conda.

## Running the costing code

With an environment set up correctly, run the following command to execute the costing code:

```bash
python3 RunCostingForCustomer.py "CATF"
```

Which, working from the `customers/CATF/` folder, will take inputs from the `DefineInputs.py` file and
output `inputs.json`, `data.json`, and `output/` processed template files.
