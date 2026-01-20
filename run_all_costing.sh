#!/bin/bash

# Script to run costing combinations for a customer.
# Usage: ./run_all_costing.sh <customer> [--mfe|--ife] [--lite] [--safety] [--full]
#   <customer>         Required customer name (e.g., CATF or woodruff)
#   --mfe              Run only for MFE fusion machine type
#   --ife              Run only for IFE fusion machine type
#   (no --mfe/--ife)   Run for both MFE and IFE
#   --lite             Only run lite reports
#   --safety           Only run safety reports
#   --lite --safety    Only run lite + safety reports
#   --full             Only run full reports
#   --full --safety    Only run full + safety reports
#   --full --lite      Invalid combination (will error)

set -e  # Exit on error

# Check if customer is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <customer> [--mfe|--ife] [--lite] [--safety] [--full]"
    exit 1
fi

CUSTOMER=$1
shift

FUSION_TYPES=("mfe" "ife")

# Flags controlling which combinations to run
RUN_LITE=false
RUN_FULL=false
SAFETY_ONLY=false

# Parse flags
while [ $# -gt 0 ]; do
    case "$1" in
        --mfe)
            FUSION_TYPES=("mfe")
            ;;
        --ife)
            FUSION_TYPES=("ife")
            ;;
        --lite)
            RUN_LITE=true
            ;;
        --full)
            RUN_FULL=true
            ;;
        --safety)
            SAFETY_ONLY=true
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 <customer> [--mfe|--ife] [--lite] [--safety] [--full]"
            exit 1
            ;;
    esac
    shift
done

# Validate incompatible combinations
if [ "$RUN_LITE" = true ] && [ "$RUN_FULL" = true ]; then
    echo "Error: --full and --lite cannot be used together."
    exit 1
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
    
    # Determine which combinations to run based on flags
    if [ "$RUN_LITE" = false ] && [ "$RUN_FULL" = false ] && [ "$SAFETY_ONLY" = false ]; then
        # Default behaviour: run all four combinations
        run_costing "$fusion_type" "" "Full report (no safety)"
        run_costing "$fusion_type" "--lite" "Lite report (no safety)"
        run_costing "$fusion_type" "--safety" "Full report (with safety)"
        run_costing "$fusion_type" "--lite --safety" "Lite report (with safety)"
    else
        if [ "$RUN_LITE" = true ] && [ "$RUN_FULL" = false ]; then
            if [ "$SAFETY_ONLY" = true ]; then
                # --lite --safety: only lite + safety
                run_costing "$fusion_type" "--lite --safety" "Lite report (with safety)"
            else
                # --lite only: lite with and without safety
                run_costing "$fusion_type" "--lite" "Lite report (no safety)"
                run_costing "$fusion_type" "--lite --safety" "Lite report (with safety)"
            fi
        elif [ "$RUN_FULL" = true ] && [ "$RUN_LITE" = false ]; then
            if [ "$SAFETY_ONLY" = true ]; then
                # --full --safety: only full + safety
                run_costing "$fusion_type" "--safety" "Full report (with safety)"
            else
                # --full only: full without safety
                run_costing "$fusion_type" "" "Full report (no safety)"
            fi
        elif [ "$RUN_LITE" = false ] && [ "$RUN_FULL" = false ] && [ "$SAFETY_ONLY" = true ]; then
            # --safety only: both full and lite safety reports
            run_costing "$fusion_type" "--safety" "Full report (with safety)"
            run_costing "$fusion_type" "--lite --safety" "Lite report (with safety)"
        fi
    fi
done

echo ""
echo "##########################################"
echo "# All costing runs completed!"
echo "##########################################"
