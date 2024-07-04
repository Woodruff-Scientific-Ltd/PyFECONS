# Set the working directory
setwd(".")

# Install devtools if not already installed
if (!requireNamespace("devtools", quietly = TRUE)) {
  install.packages("devtools")
}

# Install Kmisc from GitHub
if (!requireNamespace("Kmisc", quietly = TRUE)) {
  devtools::install_github("kevinushey/Kmisc")
}

# Load required libraries
required_packages <- c("ggplot2", "bayesm", "arm", "reshape", "nlme", "fGarch")
new_packages <- required_packages[!(required_packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) install.packages(new_packages)

# Load required packages
lapply(required_packages, library, character.only = TRUE)

# Run data prep
source("dataprep.R")

# Run the simulation
source("simulation.R")
