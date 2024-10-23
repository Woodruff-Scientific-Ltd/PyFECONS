import json
from dataclasses import is_dataclass, asdict
from enum import Enum
from pyfecons.materials import Materials


# Custom JSON encoder for specific object types
class PyfeconsEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'toDict') and callable(getattr(obj, 'toDict')):
            return obj.toDict()
        elif isinstance(obj, Enum):
            if hasattr(obj, 'display_name'):
                return {"value": obj.value, "display_name": obj.display_name}
            else:
                return obj.value  # Return just the value if there's no 'display_name'
        elif isinstance(obj, bytes):
            return ''
        return json.JSONEncoder.default(self, obj)


# Base class for serializable objects
class SerializableToJSON:
    def toDict(self):
        inputsDict = {}
        for attr_name, attr_value in self.__dict__.items():
            if not attr_name.startswith("_"):
                inputsDict[attr_name] = self._attributesToDict(attr_value)
        return inputsDict

    @staticmethod
    def _attributesToDict(obj):
        if is_dataclass(obj):
            return {key: SerializableToJSON._attributesToDict(value)
                    for key, value in asdict(obj).items() if not key.startswith("_")}
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, Materials):
            return {key: SerializableToJSON._attributesToDict(getattr(obj, key))
                    for key in dir(obj) if not key.startswith("_") and not callable(getattr(obj, key))}
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
