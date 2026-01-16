import argparse
import json
import os
import shutil
import sys

from pyfecons.helpers import load_customer_overrides
from pyfecons.serializable import PyfeconsEncoder

#################
# GATHER INPUTS #
#################

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Run costing calculations and generate report for a customer"
)
parser.add_argument(
    "reactor_type",
    type=str,
    choices=["mfe", "ife", "mif"],
    help="Reactor type: mfe, ife, or mif",
)
parser.add_argument("customer_name", type=str, help="Customer name")
parser.add_argument(
    "--lite",
    action="store_true",
    help="Generate lite report instead of full report",
)

args = parser.parse_args()
reactor_type = args.reactor_type
customer_name = args.customer_name
generate_lite = args.lite

if reactor_type not in ["mfe", "ife", "mif"]:
    print("Invalid REACTOR_TYPE: should be mfe, ife, or mif")
    sys.exit(1)

if reactor_type == "mif":
    print("REACTOR_TYPE mif not yet implemented...")
    sys.exit(1)


# Check if the customer folder exists
customer_folder = f"customers/{customer_name}/{reactor_type}"
os.makedirs(customer_folder, exist_ok=True)

# Check if DefineInputs.py exists within the customer folder
define_inputs_path = os.path.join(customer_folder, "DefineInputs.py")
if not os.path.isfile(define_inputs_path):
    print(f"ERROR: DefineInputs.py is missing in the {customer_folder}.")
    print("ERROR: Please ensure DefineInputs.py is present in the customer's folder.")
    sys.exit(1)

# Attempt to import DefineInputs and its Generate function
try:
    sys.path.append(customer_folder)
    import DefineInputs as CustomerInputs

    if "Generate" not in dir(CustomerInputs):
        raise AttributeError("ERROR: Generate function is missing in DefineInputs.py.")
except ImportError as e:
    print(e)
    print(f"ERROR: Could not import DefineInputs from {customer_folder}.")
    sys.exit(1)
except AttributeError as e:
    print(e)
    print("ERROR: Ensure DefineInputs.py contains a 'Generate' function.")
    sys.exit(1)

# Ensure Generate returns an instance of Input class
try:
    from pyfecons.inputs.all_inputs import AllInputs

    inputs = CustomerInputs.Generate()
    if not isinstance(inputs, AllInputs):
        raise TypeError(
            f"Generate function in {customer_folder} must return an instance of AllInput class."
        )
except TypeError as e:
    print(
        f"ERROR: Ensure the Generate function in {customer_folder}/DefineInputs.py returns an object of type AllInputs."
    )
    sys.exit(1)

inputDict = inputs.toDict()
# Write the inputs to a json file in the customer's folder
with open(f"{customer_folder}/inputs.json", "w", encoding="utf-8") as file:
    inputJSONstring = json.dumps(inputDict, indent=4, cls=PyfeconsEncoder)
    file.write(inputJSONstring)


#############################
# RUN THE MAIN COSTING CODE #
#############################
# this is also where the frontend would come in with an inputDict and run the main costing code

# Run the initial costing code
from pyfecons.pyfecons import (
    CreateReportContent,
    CreateReportContentLite,
    RenderFinalReport,
    RunCosting,
)

costing_data = RunCosting(inputs)
dataDict = costing_data.toDict()

# the dataDict is a dictionary carrying the calculated numbers (calculated using the inputs)
# Write the data to a JSON file in the customer's folder
with open(f"{customer_folder}/data.json", "w", encoding="utf-8") as file:
    dataJSONstring = json.dumps(dataDict, indent=4, cls=PyfeconsEncoder)
    file.write(dataJSONstring)


#########################
# HYDRATE THE TEMPLATES #
#########################

overrides = load_customer_overrides(customer_folder)

# fill in the templates and copy them to the customer's folder
if generate_lite:
    report_content = CreateReportContentLite(inputs, costing_data, overrides)
    report_filename = "report-lite"
else:
    report_content = CreateReportContent(inputs, costing_data, overrides)
    report_filename = "report"

# Save report sections to JSON for tracking changes
sections_dict = {
    section.__class__.__name__: {
        "template_file": section.template_file,
        "replacements": section.replacements,
        "figures": list(section.figures.keys()) if hasattr(section, "figures") else [],
    }
    for section in report_content.report_sections
}
sections_filename = "sections_lite.json" if generate_lite else "sections.json"
with open(f"{customer_folder}/{sections_filename}", "w", encoding="utf-8") as file:
    sectionsJSONstring = json.dumps(sections_dict, indent=4, cls=PyfeconsEncoder)
    file.write(sectionsJSONstring)

# delete the existing contents of the output folder
# Loop through all the items in the directory
output_dir = (
    f"{customer_folder}/output_lite" if generate_lite else f"{customer_folder}/output"
)
os.makedirs(output_dir, exist_ok=True)
items = os.listdir(output_dir)
if items:
    for item_name in items:
        # Create the full path to the item
        item_path = os.path.join(output_dir, item_name)

        # Check if this is a file or directory
        if os.path.isfile(item_path):
            # If it's a file, delete it
            os.remove(item_path)
        elif os.path.isdir(item_path):
            # If it's a directory, delete it and all its contents
            shutil.rmtree(item_path)
    print(f"Existing contents of {output_dir} have been deleted.")

# a dictionary with keys = name of file, value = contents
# Write the data to files in the customer's folder
with open(
    f"{output_dir}/{report_content.document_template.template_provider.template_file}",
    "w",
    encoding="utf-8",
) as file:
    file.write(report_content.document_template.contents)
for hydrated_template in report_content.hydrated_templates:
    with open(
        f"{output_dir}/{hydrated_template.template_provider.template_file}",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(hydrated_template.contents)
for tex_path, figure_bytes in report_content.figures.items():
    output_file = f"{output_dir}/{tex_path}"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "wb") as file:
        file.write(figure_bytes)

print(f"Costing run completed for {customer_name}. Data saved to {customer_folder}")


# create final pdf output
final_report = RenderFinalReport(report_content)
with open(f"{output_dir}/{report_filename}.tex", "w", encoding="utf-8") as file:
    file.write(final_report.report_tex)
with open(f"{output_dir}/{report_filename}.pdf", "wb") as file:
    file.write(final_report.report_pdf)
