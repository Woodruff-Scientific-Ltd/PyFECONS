import sys
import os
import json


#################
# GATHER INPUTS #
#################

# Check if the correct number of arguments is passed
if len(sys.argv) != 2:
    print("Usage: python3 RunCosting.py 'CUSTOMER_NAME'")
    sys.exit(1)
customer_name = sys.argv[1]

# Check if the customer folder exists
customer_folder = f"Customers/{customer_name}"
if not os.path.isdir(customer_folder):
    print(f"ERROR: Customer folder for {customer_name} does not exist.")
    print("ERROR: Please ensure the customer's folder is created under 'Customers/'.")
    sys.exit(1)

# Check if DefineInputs.py exists within the customer folder
define_inputs_path = os.path.join(customer_folder, 'DefineInputs.py')
if not os.path.isfile(define_inputs_path):
    print(f"ERROR: DefineInputs.py is missing in the {customer_folder}.")
    print("ERROR: Please ensure DefineInputs.py is present in the customer's folder.")
    sys.exit(1)

# Attempt to import DefineInputs and its Generate function
try:
    sys.path.append(customer_folder)
    import DefineInputs as CustomerInputs
    if 'Generate' not in dir(CustomerInputs):
        raise AttributeError("ERROR: Generate function is missing in DefineInputs.py.")
except ImportError:
    print(f"ERROR: Could not import DefineInputs from {customer_folder}.")
    sys.exit(1)
except AttributeError as e:
    print(e)
    print("ERROR: Ensure DefineInputs.py contains a 'Generate' function.")
    sys.exit(1)

# Ensure Generate returns an instance of Input class
try:
    from Inputs import Inputs  # Adjust this path if Input.py is located elsewhere
    inputs = CustomerInputs.Generate()
    if not isinstance(inputs, Inputs):
        raise TypeError(f"Generate function in {customer_folder} must return an instance of Input class.")
except TypeError as e:
    print(f"ERROR: Ensure the Generate function in {customer_folder}/DefineInputs.py returns an object of type Inputs.")
    sys.exit(1)

inputDict = inputs.toDict()
# Write the inputs to a json file in the customer's folder
with open(f"{customer_folder}/inputs.json", "w") as file:
    inputJSONstring = json.dumps(inputDict, indent=4)
    file.write(inputJSONstring)






#############################
# RUN THE MAIN COSTING CODE #
#############################
# this is also where the frontend would come in with an inputDict and run the main costing code
    
    # DOES NOT EXIST YET
dataDict = RunMainCosting(inputDict)
# the dataDict is a dictionary carrying the calculated numbers (calculated using the inputs)

# Write the data to a JSON file in the customer's folder
with open(f"{customer_folder}/data.json", "w") as file:
    dataJSONstring = json.dumps(dataDict, indent=4)(index=False)
    file.write(dataJSONstring)








#########################
# HYDRATE THE TEMPLATES #
#########################
    
    # DOES NOT EXIST YET
HydrateTemplates(dataDict, customer_folder)

print(f"Costing run completed for {customer_name}. Data saved to {customer_folder}")