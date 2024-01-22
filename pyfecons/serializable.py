from enum import Enum
class SerializableToJSON():

    def toDict(self):
        inputsDict = {}
        for attr_name, attr_value in self.__dict__.items():
            # Check if the attribute is an instance of a custom class (not a built-in type)
            if not isinstance(attr_value, (int, float, str, list, dict, tuple, set)):
                inputsDict[attr_name] = self._attributesToDict(attr_value)
        return inputsDict

    @staticmethod
    def _attributesToDict(obj):
        attributes = {}
        for attr in vars(obj):
            if not attr.startswith('_'):
                attr_value = getattr(obj, attr)
                if isinstance(attr_value, Enum):
                    attributes[attr] = attr_value.value
                else:
                    attributes[attr] = attr_value
        return attributes

    @classmethod
    def fromDict(cls, inputsDict):
        instance = cls()  # Creates an instance of the subclass
        for attr_name, attr_value in inputsDict.items():
            # Check if the attribute is meant for a custom class
            if hasattr(instance, attr_name) and isinstance(attr_value, dict):
                # Recursively create an instance of the custom class
                setattr(instance, attr_name,
                        cls._dictToAttributes(getattr(instance, attr_name).__class__, attr_value))
            else:
                setattr(instance, attr_name, attr_value)
        return instance

    @staticmethod
    def _dictToAttributes(cls, attr_dict):
        obj = cls()
        for attr, value in attr_dict.items():
            # Get the attribute type from the class
            attr_type = getattr(cls, attr).__class__

            # Check if the attribute type is a subclass of Enum
            if issubclass(attr_type, Enum):
                enum_value = attr_type(value)  # Convert string back to enum
                setattr(obj, attr, enum_value)
            else:
                setattr(obj, attr, value)

        return obj
