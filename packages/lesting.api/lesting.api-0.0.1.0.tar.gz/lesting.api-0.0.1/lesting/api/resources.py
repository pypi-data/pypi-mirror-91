from typing import Callable, Dict, List, Any
from .schemas import Schema
from inspect import Signature

class Method:

    base: "Resource"
    name: str
    func: Callable
    method: str
    path: List[str]
    signature: Signature
    parameters: Dict[str, Schema]
    response: Schema

    def __init__(self, base: "Resource", func: Callable, method: str) -> None:
        self.name = func.__name__
        self.func = func
        self.method = method
        self.path = base.path + [self.name]
        self.signature = Signature.from_callable(func)
        self.parameters = {name: Schema.Meta.clean(self.signature.parameters[name].annotation, base.schemas) for name in list(self.signature.parameters)}
        self.response = Schema.Meta.clean(self.signature.return_annotation, base.schemas)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.func(*args, **kwds)

    def format(self):
        return {
            "type": "method",
            "name": self.name,
            "method": self.method,
            "path": "/".join(self.path),
            "parameters": {name: parameter.format() for name, parameter in self.parameters.items()},
            "response": self.response.format()
        }

class Resource:

    base: "Resource"
    name: str
    path: List[str]
    schemas: Dict[str, Schema]
    resources: Dict[str, "Resource"]

    def __init__(self, base: "Resource", name: str) -> None:
        self.base = base
        self.name = name
        self.resources = {}

    def __getattr__(self, name: str):
        return self.resources.get(name)

    @property
    def path(self) -> List[str]:
        return self.base.path + [self.name]
    
    @property
    def schemas(self):
        return self.base.schemas

    def resource(self, name: str) -> "Resource":
        return self.resources.setdefault(name, Resource(self, name))

    def method(self, method: str):
        def wrapper(func):
            return self.resources.setdefault(func.__name__, Method(self, func, method))
        return wrapper

    def format(self):
        return {
            "type": "resource",
            "name": self.name,
            "resources": {name: resource.format() for name, resource in self.resources.items()}
        }

class Service(Resource):

    name: str
    version: str
    base: str
    path: List[str] = None
    schemas: Dict[str, Schema] = None

    def __init__(self, name: str, version: str, base: str = "http://127.0.0.1:80") -> None:
        self.name = name
        self.version = version
        self.base = base
        self.resources = {}
        self.schemas = {}
        self.path = ["", self.name, self.version]

    def __getattr__(self, name: str):
        return self.resources.get(name, self.schemas.get(name))

    def format(self):
        return {
            "type": "service",
            "name": self.name,
            "version": self.version,
            "base": self.base,
            "schemas": {name: schema.full() for name, schema in self.schemas.items()},
            "resources": {name: resource.format() for name, resource in self.resources.items()}
        }