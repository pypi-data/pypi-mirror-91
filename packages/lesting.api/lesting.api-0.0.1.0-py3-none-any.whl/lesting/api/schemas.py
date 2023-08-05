__all__ = [
    "Struct",
    "Object"
]

from typing import Optional, Union, Tuple, Dict, List, Any
from itertools import zip_longest

class Schema:
    _name: str

    schemas: Dict[str, "Schema"]

    class Meta(type):

        Map: Dict[Union[str, type], "Schema"] = {}

        def __new__(cls, name: str, bases: Tuple[Union["Schema", type], ...], namespace: Dict[str, Any]):
            return super().__new__(cls, name, bases, bases[0].build(namespace))

        @classmethod
        def register(cls, schema: "Schema") -> None:
            cls.Map[schema._name] = schema

        @classmethod
        def clean(cls, object: Any, schemas: Optional[Dict[str, "Schema"]] = None) -> None:
            if isinstance(object, type):
                if object in cls.Map:
                    return cls.Map[object]
                elif issubclass(object, Schema):
                    schemas.update(object.schemas)
                    if issubclass(object, Struct) and not issubclass(object, Object):
                        schemas[object.__name__] = object
                    return object
            if isinstance(object, Schema):
                schemas.update(object.schemas)
                return object
            if object.__class__ in cls.Map:
                return cls.Map[object.__class__]
            if object in cls.Map:
                return object
            raise TypeError(object)

        @classmethod
        def make(cls, document: Dict[str, Any], schemas: Optional[Dict[str, "Schema"]] = None) -> "Schema":
            if document["type"] in cls.Map:
                return cls.Map[document["type"]].make(document, schemas)
            raise TypeError("invaild schema `%s`" % document["type"])

    @classmethod
    def build(cls, namespace: Dict[str, Any]) -> Dict[str, Any]:
        return {**{"schemas": {}}, **namespace}

    @classmethod
    def make(cls, document: Dict[str, Any]) -> "Schema":
        raise NotImplementedError

    @classmethod
    def new(cls, value: Any) -> Any:
        raise NotImplementedError

    @classmethod
    def dump(cls, value: Any) -> Any:
        raise NotImplementedError

    @classmethod
    def format(cls) -> Dict[str, str]:
        return {
            "type": cls._name
        }

class Struct(Schema, metaclass = Schema.Meta):
    _name = "struct"

    fields: Dict[str, Schema]

    def __init__(self, *args, **kwargs) -> None:
        for field, value in zip_longest(self.fields.items(), args):
            if value is not None:
                kwargs[field[0]] = value
            if getattr(field[1], "required", True) and field[0] not in kwargs:
                raise ValueError("`%s` was missing" % (field[0]))
        for name, value in kwargs.items():
            setattr(self, name, value)

    @classmethod
    def build(cls, namespace: Dict[str, Any]) -> Dict[str, Any]:
        schemas = namespace.setdefault("schemas", {})
        fields: Dict[str, "Schema"] = namespace.setdefault("fields", {})
        fields.update({key: Schema.Meta.clean(val, schemas) for key, val in namespace.get("__annotations__", {}).items()})
        return namespace

    @classmethod
    def make(cls, document: Dict[str, Any], schemas: Dict[str, Schema]):
        if "ref" in document:
            return schemas[document["ref"]]
        return type(document["name"], (cls,), {
            "fields": {name: Schema.Meta.make(field, schemas) for name, field in document["fields"].items()},
            "schemas": {}
        })

    @classmethod
    def new(cls, value: Any) -> "Struct":
        return cls(**value)

    @classmethod
    def dump(cls, value):
        assert isinstance(value, cls), "value must be `%s` not `%s`" % (cls.__name__, value.__class__.__name__)
        return {name: field.dump(getattr(value, name)) for name, field in value.fields.items() if hasattr(value, name)}

    @classmethod
    def format(cls) -> Dict[str, str]:
        return {
            "type": cls._name,
            "ref": cls.__name__
        }

    @classmethod
    def full(cls) -> Dict[str, Any]:
        return {
            "type": cls._name,
            "name": cls.__name__,
            "fields": {name: field.format() for name, field in cls.fields.items()}
        }

    def __setattr__(self, name: str, value: Any) -> None:
        assert name in self.fields
        object.__setattr__(self, name, value)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, ", ".join(["%s=%r" % (field, getattr(self, field, None)) for field in self.fields.keys()]))

Schema.Meta.register(Struct)

class Object(Struct):
    _name = "object"

    @classmethod
    def format(cls) -> Dict[str, Any]:
        return super().full()

    @classmethod
    def quick(cls, name: str, fields: Dict[str, Any]) -> "Object":
        return type(name, (Object,), {"__annotations__": fields})
    
    @classmethod
    def dump(cls, value):
        return super().dump(cls(**value))

Schema.Meta.register(Object)