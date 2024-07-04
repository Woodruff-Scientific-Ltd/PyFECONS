#!/bin/bash

# Activate the Conda environment
# conda activate r_env

# Download the RcppArmadillo package source
curl -O https://cran.r-project.org/src/contrib/RcppArmadillo_0.12.8.4.0.tar.gz

# Extract the source code
tar -xzf RcppArmadillo_0.12.8.4.0.tar.gz
cd RcppArmadillo

# Perform find and replace of 'std::log1p' with 'Rlog1p' in the entire directory
find . -type f -exec perl -pi -e 's/std::log1p/Rlog1p/g' {} +

# Install the modified package
R CMD INSTALL .
cd ..

# Install bayesm package
curl -O https://cran.rstudio.com/src/contrib/bayesm_3.1-6.tar.gz
tar -xzf bayesm_3.1-6.tar.gz
cd bayesm
R CMD INSTALL .
cd ..

# cleanup
rm RcppArmadillo_0.12.8.4.0.tar.gz
rm -rf RcppArmadillo
rm bayesm_3.1-6.tar.gz
rm -rf bayesm