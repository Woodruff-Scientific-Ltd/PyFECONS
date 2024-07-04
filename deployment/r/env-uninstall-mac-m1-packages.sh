#!/bin/bash

# Activate the Conda environment
# conda activate r_env

# Run R commands to uninstall the packages
Rscript -e "remove.packages('RcppArmadillo')" -e "remove.packages('bayesm')"