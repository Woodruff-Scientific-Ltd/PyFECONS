import json
from dataclasses import is_dataclass, asdict
from enum import Enum


# This is needed because our custom json serializer is not handling lists correctly
class PyfeconsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            # Check if the enum has a 'display_name' attribute
            if hasattr(obj, 'display_name'):
                return {"value": obj.value, "display_name": obj.display_name}
            else:
                return obj.value  # Return just the value if there's no 'display_name'
        # Let the base class default method raise the TypeError for other types
        return json.JSONEncoder.default(self, obj)


class SerializableToJSON():

    def toDict(self):
        inputsDict = {}
        for attr_name, attr_value in self.__dict__.items():
            # Check if the attribute is an instance of a custom class (not a built-in type)
            inputsDict[attr_name] = self._attributesToDict(attr_value)
        return inputsDict

    @staticmethod
    def _attributesToDict(obj):
        if is_dataclass(obj):
            return {key: SerializableToJSON._attributesToDict(value) for key, value in asdict(obj).items()}
        elif isinstance(obj, Enum):
            return obj.value
        elif type(obj) in [int, float, str, list, dict, tuple, set]:
            return obj
        # handle Unit classes which only inherit from one primitive
        elif (len(obj.__class__.__bases__) > 0
              and obj.__class__.__bases__[0] in [int, float, str, list, dict, tuple, set]):
            return obj
        elif hasattr(obj, '__dict__'):
            return {key: SerializableToJSON._attributesToDict(value)
                    for key, value in obj.__dict__.items() if not key.startswith('_')}
        else:
            return obj

    @classmethod
    def fromDict(cls, inputsDict):
        instance = cls()  # Creates an instance of the subclass
        for attr_name, attr_value in inputsDict.items():
            if hasattr(instance, attr_name):
                attr = getattr(instance, attr_name)
                if isinstance(attr_value, dict):
                    if is_dataclass(attr.__class__):
                        setattr(instance, attr_name, attr.__class__(**attr_value))
                    else:
                        setattr(instance, attr_name, cls._dictToAttributes(attr.__class__, attr_value))
                else:
                    setattr(instance, attr_name, attr_value)
        return instance

    @staticmethod
    def _dictToAttributes(cls, attr_dict):
        obj = cls()
        for attr, value in attr_dict.items():
            attr_type = getattr(cls, attr).__class__
            if issubclass(attr_type, Enum):
                enum_value = attr_type(value)  # Convert string back to enum
                setattr(obj, attr, enum_value)
            else:
                setattr(obj, attr, value)
        return obj
