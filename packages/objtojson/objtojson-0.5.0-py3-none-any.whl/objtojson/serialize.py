import inspect
import json
import os
from typing import Dict, List, Any


class SerializeError(Exception):
    pass


class _SerializeMeta(type):
    """ Metaclass for classes that may be json-serialized. Do not use directly.
    """
    OBJECT_HOOKS = []
    SERIALIZED_ATTRIBUTES: Dict[str, List[str]] = {}

    def __new__(mcs, name, bases, dct):
        clazz = super().__new__(mcs, name, bases, dct)
        if not name.startswith('_'):
            assert name not in _SerializeMeta.SERIALIZED_ATTRIBUTES, f'Class with name {name} already registered!'
            clazz.Serialize, clazz.Deserialize, clazz.FromJson = _SerializeMeta.__GetSerializerMethods(clazz)
            # by default use args and kwargs of __init__ for serialization
            # TODO allow custom specification of serialized attributes
            _SerializeMeta.SERIALIZED_ATTRIBUTES[name] = _SerializeMeta.__ExtractArgs(clazz.__init__)
            clazz.__eq__ = _SerializeMeta.__GetEqMethod(clazz)
            _SerializeMeta.OBJECT_HOOKS.append(clazz.Deserialize)
        return clazz

    @classmethod
    def __GetSerializerMethods(cls, clazz):
        serializedName = f'__{clazz.__name__.lower()}__'
        clazz.SERIALIZED_NAME = serializedName
        def Deserialize(dct):
            """ Create new object from JSON string """
            if serializedName in dct:
                initValues = {}
                for attrName, value in dct[serializedName].items():
                    if attrName in clazz.CUSTOM_SERIALIZERS:
                        initValues[attrName] = clazz.CUSTOM_SERIALIZERS[attrName]().Deserialize(value)
                    else:
                        initValues[attrName] = value
                result = clazz(**initValues)
                return result
        def Serialize(slf):
            """ Convert object to JSON string"""
            attributes = {}
            for attrName in _SerializeMeta.SERIALIZED_ATTRIBUTES[clazz.__name__]:
                obj = getattr(slf, attrName)
                if attrName in slf.CUSTOM_SERIALIZERS:
                    value = slf.CUSTOM_SERIALIZERS[attrName]().Serialize(obj)
                else:
                    value = cls.SerializeObject(obj)
                attributes[attrName] = value
            return {serializedName: attributes}
        def FromJson(slf, jsonString):
            """ In-place deserialization of an object """
            result = Serializer.FromJson(jsonString)
            if result.__class__ is not slf.__class__:
                raise ValueError(f'Deserialized objects class does not match {slf.__class__}. Got:\n{result.__class__} ({result})')
            Serializer.CopyAttributes(result, slf)
            slf.AfterDeserialize()

        return Serialize, Deserialize, FromJson

    @staticmethod
    def SerializeObject(obj):
        if isinstance(obj, _Serialized):
            value = obj.Serialize()

        elif isinstance(obj, dict):
            savedDict = obj.copy()
            for k, v in obj.copy().items():
                serializedKey = _SerializeMeta.SerializeObject(k)
                if not isinstance(serializedKey, str):
                    raise SerializeError(f'Only strings are allowed as dict keys. '
                                         f'Got {type(serializedKey)}')
                savedDict[serializedKey] = _SerializeMeta.SerializeObject(v)
            value = savedDict

        elif isinstance(obj, (list, tuple)):
            savedList = list(obj)
            for i, v in enumerate(obj):
                savedList[i] = _SerializeMeta.SerializeObject(v)
            value = savedList

        elif obj is None or isinstance(obj, (str, float, int, bool)):
            # use as-is
            value = obj

        else:
            raise SerializeError(f'No serialization method available for object of type {type(obj)}')
        return value

    @classmethod
    def __ExtractArgs(cls, method):
        argSpec = inspect.getfullargspec(method)
        argNames = argSpec.args + argSpec.kwonlyargs
        return [a for a in argNames if a != 'self']

    @classmethod
    def __GetEqMethod(cls, clazz):
        def Eq(slf: '_Serialized', other: Any):
            return (isinstance(other, _Serialized)
                    and slf.Serialize() == other.Serialize())
        return Eq

    @classmethod
    def ObjectHook(cls, dct):
        for deser in cls.OBJECT_HOOKS:
            obj = deser(dct)
            if obj is not None:
                return obj
        return dct


class CustomSerializer:
    """ Derive from this class to implement a custom Object->JSON->Object
    serializer/deserializer and declare it in the CUSTOM_SERIALIZERS class variable
    of the class that contains fields of this type """
    def Serialize(self, obj: Any) -> str:
        raise NotImplementedError

    def Deserialize(self, jsonString: str) -> Any:
        raise NotImplementedError


class _Serialized(metaclass=_SerializeMeta):
    """ Base class for objects that should be automatically be serializable.

    How it works? Any argument to __init__ will be assumed to have an instance variable
    with the same name. These will be detected and stored to JSON.
    """
    SERIALIZED_NAME: str = ''  # Will be initialized automatically. Do not overwrite!
    CUSTOM_SERIALIZERS: Dict[str, CustomSerializer] = {}

    @classmethod
    def Deserialize(cls, dct):
        """ Dummy method -> Automatically implemented in metaclass """
        return None

    def Serialize(self) -> Dict:
        """ Dummy method -> Automatically implemented in metaclass """
        return {}

    def AfterDeserialize(self):
        """ Override to perform custom actions after deserialization """
        pass

    def FromJson(self, jsonString: str):
        """ Dummy method -> Automatically implemented in metaclass """
        pass

    def ToJson(self) -> str:
        return Serializer.ToJson(self)


class Serializer:
    """ Class with helper functions for serializing objects to and from JSON
    """

    @classmethod
    def FromJson(cls, jsonString: str) -> _Serialized:
        return json.loads(jsonString, object_hook=_SerializeMeta.ObjectHook)

    @classmethod
    def ToJson(cls, obj: _Serialized) -> str:
        try:
            return json.dumps(obj.Serialize(), indent=4)
        except Exception as e:
            raise SerializeError(f'Serializing failed for\n{obj.Serialize()}') from e

    @classmethod
    def Save(cls, path: str, obj: _Serialized):
        dirName = os.path.dirname(path)
        os.makedirs(dirName, exist_ok=True)
        with open(path, 'w') as f:
            f.write(cls.ToJson(obj))

    @classmethod
    def Load(cls, path) -> _Serialized:
        with open(path) as f:
            return cls.FromJson(f.read())

    @classmethod
    def CopyAttributes(cls, fromObject: _Serialized, toObject: _Serialized):
        assert fromObject.__class__ is toObject.__class__
        assert isinstance(fromObject, _Serialized)
        for attrName in _SerializeMeta.SERIALIZED_ATTRIBUTES[fromObject.__class__.__name__]:
            fromValue = getattr(fromObject, attrName)
            setattr(toObject, attrName, fromValue)

