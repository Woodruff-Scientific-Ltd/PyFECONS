# Electricity Deployment Simulation

## Download Data files

Data files are located in [Google Drive](https://drive.google.com/drive/folders/1O7q-9J_2qYRtgbwDxbOpgZETMU3DMRrh?usp=drive_link).
Please download and add them to the `r/data` directory.

## Set up R with Conda

To use R studio seamlessly with Conda.

### Conda Commands

```
# create environment - only need to do this once or every time after deleting the environment 
conda env create -f environment.yml

# list environments
conda env list

# activate pyfecons environment
conda activate r_env

# updating conda environment (after adidng or removing dependencies)
conda env update -f environment.yml

# deactivating the Conda environment
conda deactivate

# delete environment - to reinstall fresh 
conda env remove -n r_env

```

### Set R path

This is needed for R studio to find the conda downloaded version of R.

Check if the variable is set in a terminal with:
```
echo $RSTUDIO_WHICH_R
```

With the `r_env` conda environment activated, you can find the installed R path with: 
```
which R
```

Then set the env variable with the output like so:
```
export RSTUDIO_WHICH_R="YOUR_CONDA_INSTALL_PATH/envs/r_env/bin/R"
```

### Open R studio

Run the following:
```
open -a RStudio
```

