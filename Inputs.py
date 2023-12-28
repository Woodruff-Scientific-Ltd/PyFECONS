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
    def __init__(self):
        # Don't forget to add an instance of new subclasses here
        self.basic = self.Basic()
        self.blanket = self.Blanket()


    class Basic:
        def __init__(self):
            self.timeToReplace:float = None #years
            self.downTime:float = None # years
            self.reactorType:int = None #2 is IFE, 1 is MFE, 3 is MIF
            self.N_mod:int = None # number of modules
            self.AM:int = None # dunno
            self.constructionTime:float #years

    class Blanket:
        def __init__(self):
            self.firstWall:int = None
            self.blanketType:int = None
            self.primaryCoolant:int = None
            self.secondaryCoolant:int = None
            self.neutronMultiplier:int = None
            self.structure:int = None


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
