#!/bin/bash

# Script to run all costing combinations for a customer
# Usage: ./run_all_costing.sh <customer> [--mfe|--ife]

set -e  # Exit on error

# Check if customer is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <customer> [--mfe|--ife]"
    echo "  customer: Required customer name (e.g., CATF or woodruff)"
    echo "  --mfe:    Run only for MFE fusion machine type"
    echo "  --ife:    Run only for IFE fusion machine type"
    echo "  (no flag): Run for both MFE and IFE"
    exit 1
fi

CUSTOMER=$1
FUSION_TYPES=()

# Parse optional fusion machine type
if [ "$2" == "--mfe" ]; then
    FUSION_TYPES=("mfe")
elif [ "$2" == "--ife" ]; then
    FUSION_TYPES=("ife")
else
    # Default: run for both MFE and IFE
    FUSION_TYPES=("mfe" "ife")
fi

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/RunCostingForCustomer.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: RunCostingForCustomer.py not found at $PYTHON_SCRIPT"
    exit 1
fi

# Function to run costing with specified flags
run_costing() {
    local fusion_type=$1
    local flags=$2
    local description=$3
    
    echo ""
    echo "=========================================="
    echo "Running: $fusion_type $description"
    echo "Command: python $PYTHON_SCRIPT $fusion_type $CUSTOMER $flags"
    echo "=========================================="
    
    python "$PYTHON_SCRIPT" "$fusion_type" "$CUSTOMER" $flags
}

# Run all combinations for each fusion machine type
for fusion_type in "${FUSION_TYPES[@]}"; do
    echo ""
    echo "##########################################"
    echo "# Processing $fusion_type for customer: $CUSTOMER"
    echo "##########################################"
    
    # Run 4 combinations:
    # 1. No flags (full report, no safety)
    run_costing "$fusion_type" "" "Full report (no safety)"
    
    # 2. --lite (lite report, no safety)
    run_costing "$fusion_type" "--lite" "Lite report (no safety)"
    
    # 3. --safety (full report, with safety)
    run_costing "$fusion_type" "--safety" "Full report (with safety)"
    
    # 4. --lite --safety (lite report, with safety)
    run_costing "$fusion_type" "--lite --safety" "Lite report (with safety)"
done

echo ""
echo "##########################################"
echo "# All costing runs completed!"
echo "##########################################"
