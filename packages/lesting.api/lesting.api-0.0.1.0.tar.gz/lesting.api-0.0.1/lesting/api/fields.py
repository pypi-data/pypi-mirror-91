__all__ = [
    "String",
    "Integer",
    "Boolean",
    "Array",
    "Map",
    "NotRequired"
]

from typing import Type, List, Dict, Any
from .schemas import Schema

class Field(Schema, metaclass = Schema.Meta):
    _type: Type

    @staticmethod
    def register(field: "Field"):
        Schema.Meta.register(field)
        Schema.Meta.Map[field._type] = field

    @classmethod
    def make(cls, document: Dict[str, Any], schemas: Dict[str, Schema]) -> "Field":
        if document.get("required", True) == False:
            return NotRequired(cls)
        return cls

    @classmethod
    def new(cls, value: Any) -> Any:
        assert isinstance(value, cls._type), "value must be `%s` not `%s`" % (cls._type.__name__, value.__class__.__name__)
        return value

    @classmethod
    def dump(cls, value: Any) -> Any:
        assert isinstance(value, cls._type), "value must be `%s` not `%s`" % (cls._type.__name__, value.__class__.__name__)
        return value

class String(Field):
    _name = "string"
    _type = str

Field.register(String)

class Integer(Field):
    _name = "integer"
    _type = int

    @classmethod
    def new(cls, value: Any) -> int:
        if isinstance(value, str) and value.isdigit():
            value = int(value)
        return super().new(value)

Field.register(Integer)

class Boolean(Field):
    _name = "boolean"
    _type = bool

Field.register(Boolean)

class Array(Field):
    _name = "array"
    _type = list

    item: Schema

    def __init__(self, item: Field) -> None:
        self.item = Schema.Meta.clean(item, self.schemas)

    @classmethod
    def make(cls, document: Dict[str, Any], schemas: Dict[str, Schema]) -> "Array":
        return cls(Schema.Meta.make(document["item"], schemas))

    def new(self, value: List[Any]) -> List[Schema]:
        return [self.item.new(value) for value in value]

    def format(self) -> Dict[str, Any]:
        return {
            "type": self._name,
            "item": self.item.format()
        }

    def dump(self, value: List[Any]) -> List[Any]:
        return [self.item.dump(item) for item in super().dump(value)]

Field.register(Array)

class Map(Field):
    _name = "map"
    _type = dict

    key: Schema
    value: Schema

    def __init__(self, key: Field, value: Field) -> None:
        self.key = Schema.Meta.clean(key, self.schemas)
        self.value = Schema.Meta.clean(value, self.schemas)

    @classmethod
    def make(cls, document: Dict[str, Any], schemas: Dict[str, Schema]) -> "Map":
        return cls(Schema.Meta.make(document["key"], schemas), Schema.Meta.make(document["value"], schemas))

    def new(self, value: Dict[Any, Any]) -> Dict[Schema, Schema]:
        return {self.key.new(key): self.value.new(value) for key, value in value.items()}

    def format(self) -> Dict[str, Any]:
        return {
            "type": self._name,
            "key": self.key.format(),
            "value": self.value.format()
        }

    def dump(self, value: Dict[Any, Any]) -> Dict[Any, Any]:
        return {self.key.dump(key): self.value.dump(value) for key, value in super().dump(value).items()}

Field.register(Map)

class ANY(Field):
    _name = "any"
    _type = type(None)

    @classmethod
    def dump(cls, value: Any) -> Any:
        return value

Field.register(ANY)

class NotRequired(Field):
    required = False

    object: Schema

    def __init__(self, object: Any) -> None:
        self.schemas = {}
        self.object = Schema.Meta.clean(object, self.schemas)

    def dump(self, value):
        return self.object.dump(value)

    def format(self):
        return {**{"required": False}, **self.object.format()}