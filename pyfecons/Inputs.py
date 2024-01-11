# This class will contain every possible input
# It will not contain information about which inputs will actually used by the costing code and which ones won't
# The DefineInputs.py script in each customer folder is in charge of making sure all of the appropriate inputs are set
# The costing code itself should throw appropriate errors when necessary inputs are not set
# The logical flow of inputs & inputs dependencies will be documented here
# https://docs.google.com/spreadsheets/d/115j-R-XZX9JI_VGt4AR7T3fZ91Qdmtc-WfEg_CpSlKE/edit?usp=sharing
# The units, descriptions, and expected values will also be documented on the spreadsheet

# The classes within Inputs must maintain their own toDict function
# In addition, the Inputs class itself maintains its own toDict function that calls upon the sublcasses
class Inputs:
    class CustomerInfo:
        def __init__(self, name: str = ''):
            self.name = name

    class Basic:
        def __init__(self,
                     time_to_replace: float = 0.0,
                     down_time: float = 0.0,
                     reactor_type: int = 1,
                     n_mod: int = 1,
                     am: int = 0,
                     construction_time: float = 0.0):
            self.timeToReplace = time_to_replace
            self.downTime = down_time
            self.reactorType = reactor_type
            self.n_mod = n_mod
            self.am = am
            self.constructionTime = construction_time

    class Blanket:
        def __init__(self,
                     first_wall: int = 0,
                     blanket_type: int = 0,
                     primary_coolant: int = 0,
                     secondary_coolant: int = 0,
                     neutron_multiplier: int = 0,
                     structure: int = 0):
            self.first_wall: int = first_wall
            self.blanket_ype: int = blanket_type
            self.primary_coolant: int = primary_coolant
            self.secondary_coolant: int = secondary_coolant
            self.neutron_multiplier: int = neutron_multiplier
            self.structure: int = structure

    def __init__(self,
                 customer_info: CustomerInfo = CustomerInfo(),
                 basic: Basic = Basic(),
                 blanket: Blanket = Blanket()):
        self.customer_info = customer_info
        self.basic = basic
        self.blanket = blanket

    def toDict(self):
        inputsDict = {}
        for attr_name, attr_value in self.__dict__.items():
            # Check if the attribute is an instance of a custom class (not a built-in type)
            if not isinstance(attr_value, (int, float, str, list, dict, tuple, set)):
                inputsDict[attr_name] = self._attributesToDict(attr_value)
        return inputsDict

    @staticmethod
    def _attributesToDict(obj):
        return {attr: getattr(obj, attr) for attr in vars(obj) if not attr.startswith('_')}

    @staticmethod
    def fromDict(inputsDict):
        instance = Inputs()
        for attr_name, attr_value in inputsDict.items():
            # Check if the attribute is meant for a custom class
            if hasattr(instance, attr_name) and isinstance(attr_value, dict):
                # Recursively create an instance of the custom class
                setattr(instance, attr_name,
                        Inputs._dictToAttributes(getattr(instance, attr_name).__class__, attr_value))
            else:
                setattr(instance, attr_name, attr_value)
        return instance

    @staticmethod
    def _dictToAttributes(cls, attr_dict):
        obj = cls()
        for attr, value in attr_dict.items():
            setattr(obj, attr, value)
        return obj
