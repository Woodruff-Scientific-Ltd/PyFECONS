import sys
import os
import json
import shutil

from pyfecons.helpers import load_customer_overrides
from pyfecons.serializable import PyfeconsEncoder

#################
# GATHER INPUTS #
#################

# Check if the correct number of arguments is passed
if len(sys.argv) != 3:
    print("Invalid arguments.")
    print("Usage: python3 RunCosting.py REACTOR_TYPE CUSTOMER_NAME")
    sys.exit(1)
reactor_type = sys.argv[1]
customer_name = sys.argv[2]

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
    from pyfecons.inputs import (
        Inputs,
    )  # Adjust this path if Input.py is located elsewhere

    inputs = CustomerInputs.Generate()
    if not isinstance(inputs, Inputs):
        raise TypeError(
            f"Generate function in {customer_folder} must return an instance of Input class."
        )
except TypeError as e:
    print(
        f"ERROR: Ensure the Generate function in {customer_folder}/DefineInputs.py returns an object of type Inputs."
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
from pyfecons.pyfecons import RunCosting, CreateReportContent, RenderFinalReport

costing_data = RunCosting(inputs)
dataDict = costing_data.data.toDict()

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
report_content = CreateReportContent(inputs, costing_data, overrides)


# delete the existing contents of the output folder
# Loop through all the items in the directory
output_dir = f"{customer_folder}/output"
os.makedirs(output_dir, exist_ok=True)
for item_name in os.listdir(output_dir):
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
    f"{customer_folder}/output/{report_content.document_template.template_provider.template_file}",
    "w",
    encoding="utf-8",
) as file:
    file.write(report_content.document_template.contents)
for hydrated_template in report_content.hydrated_templates:
    with open(
        f"{customer_folder}/output/{hydrated_template.template_provider.template_file}",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(hydrated_template.contents)
for tex_path, figure_bytes in report_content.figures.items():
    output_file = f"{customer_folder}/output/{tex_path}"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "wb") as file:
        file.write(figure_bytes)

print(f"Costing run completed for {customer_name}. Data saved to {customer_folder}")


# create final pdf output
final_report = RenderFinalReport(report_content)
with open(f"{customer_folder}/output/report.tex", "w", encoding="utf-8") as file:
    file.write(final_report.report_tex)
with open(f"{customer_folder}/output/report.pdf", "wb") as file:
    file.write(final_report.report_pdf)
