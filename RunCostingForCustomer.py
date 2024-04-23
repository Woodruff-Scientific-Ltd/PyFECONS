import sys
import os
import json
import shutil

from pyfecons.serializable import PyfeconsEncoder

#################
# GATHER INPUTS #
#################

# Check if the correct number of arguments is passed
if len(sys.argv) != 2:
    print("Usage: python3 RunCosting.py 'CUSTOMER_NAME'")
    sys.exit(1)
customer_name = sys.argv[1]

# Check if the customer folder exists
customerFolder = f"customers/{customer_name}"
if not os.path.isdir(customerFolder):
    print(f"ERROR: Customer folder for {customer_name} does not exist.")
    print("ERROR: Please ensure the customer's folder is created under 'customers/'.")
    sys.exit(1)

# Check if DefineInputs.py exists within the customer folder
define_inputs_path = os.path.join(customerFolder, 'DefineInputs.py')
if not os.path.isfile(define_inputs_path):
    print(f"ERROR: DefineInputs.py is missing in the {customerFolder}.")
    print("ERROR: Please ensure DefineInputs.py is present in the customer's folder.")
    sys.exit(1)

# Attempt to import DefineInputs and its Generate function
try:
    sys.path.append(customerFolder)
    import DefineInputs as CustomerInputs
    if 'Generate' not in dir(CustomerInputs):
        raise AttributeError("ERROR: Generate function is missing in DefineInputs.py.")
except ImportError as e:
    print(e)
    print(f"ERROR: Could not import DefineInputs from {customerFolder}.")
    sys.exit(1)
except AttributeError as e:
    print(e)
    print("ERROR: Ensure DefineInputs.py contains a 'Generate' function.")
    sys.exit(1)

# Ensure Generate returns an instance of Input class
try:
    from pyfecons.inputs import Inputs  # Adjust this path if Input.py is located elsewhere
    inputs = CustomerInputs.Generate()
    if not isinstance(inputs, Inputs):
        raise TypeError(f"Generate function in {customerFolder} must return an instance of Input class.")
except TypeError as e:
    print(f"ERROR: Ensure the Generate function in {customerFolder}/DefineInputs.py returns an object of type Inputs.")
    sys.exit(1)

inputDict = inputs.toDict()
# Write the inputs to a json file in the customer's folder
with open(f"{customerFolder}/inputs.json", "w") as file:
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
with open(f"{customerFolder}/data.json", "w") as file:
    dataJSONstring = json.dumps(dataDict, indent=4, cls=PyfeconsEncoder)
    file.write(dataJSONstring)








#########################
# HYDRATE THE TEMPLATES #
#########################

# fill in the templates and copy them to the customer's folder
report_content = CreateReportContent(inputs, costing_data)

# delete the existing contents of the output folder
# Loop through all the items in the directory
outputDir = f"{customerFolder}/output"
for item_name in os.listdir(outputDir):
    # Create the full path to the item
    item_path = os.path.join(outputDir, item_name)
    
    # Check if this is a file or directory
    if os.path.isfile(item_path):
        # If it's a file, delete it
        os.remove(item_path)
    elif os.path.isdir(item_path):
        # If it's a directory, delete it and all its contents
        shutil.rmtree(item_path)
print(f"Existing contents of {outputDir} have been deleted.")

# a dictionary with keys = name of file, value = contents
# Write the data to files in the customer's folder
for hydrated_template in report_content.hydrated_templates:
    with open(f"{customerFolder}/output/{hydrated_template.template_provider.template_file}", "w") as file:
        file.write(hydrated_template.contents)

print(f"Costing run completed for {customer_name}. Data saved to {customerFolder}")


# create final pdf output
final_report = RenderFinalReport(report_content)
with open(f"{customerFolder}/output/report.tex", "w") as file:
    file.write(final_report.report_tex)
with open(f"{customerFolder}/output/report.pdf", "wb") as file:
    file.write(final_report.report_pdf)